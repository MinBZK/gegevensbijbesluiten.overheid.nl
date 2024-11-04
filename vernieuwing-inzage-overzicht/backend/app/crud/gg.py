import logging
from typing import List, Sequence

from sqlalchemy import (
    and_,
    desc,
    func,
    or_,
    select,
    text,
)
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql.expression import (
    case,
)

import app.models as models
import app.schemas as schemas
from app.core.config import CURRENT_VERSION, PUBLICATION_RANGE
from app.crud.tls_search import build_filters_gg, get_similarity_search_clause, prep_search_for_query

# Setup logger
logger = logging.getLogger(__name__)


def get_all(
    db: Session,
) -> Sequence[models.gg.Gg]:
    """Return all (child) gg's"""
    return (
        db.execute(
            select(models.gg.Gg).filter(models.gg.Gg.parent_gg_entity.any()).filter(models.gg.Gg.gst_gg_entity.has())
        )
        .scalars()
        .all()
    )


def get_details(db: Session, gg_upc: int) -> schemas.details.GgDetails:
    """
    Get details of a single selected Gg
    """
    gg = models.gg.Gg
    evtp_version = models.evtp.EvtpVersion
    gst_gg = models.gst.GstGg
    evtp_gst = models.evtp.EvtpGst
    gst = models.gst.Gst
    oe = models.oe.Oe

    # Fetch all connected gst's
    selected_gg = db.execute(select(gg).filter(gg.gg_upc == gg_upc)).scalars().one()

    _gst_publicated = (
        select(evtp_gst.gst_cd)
        .join(
            evtp_version,
            and_(
                evtp_version.evtp_cd == evtp_gst.evtp_cd,
                evtp_version.ts_start < evtp_gst.ts_end,
                evtp_version.ts_end > evtp_gst.ts_start,
                evtp_version.ts_end > func.now(),
                evtp_version.ts_start < func.now(),
            ),
        )
        .filter(evtp_version.id_publicatiestatus.in_(PUBLICATION_RANGE))
        .filter(evtp_version.huidige_versie.in_(CURRENT_VERSION))
        .subquery()
    )

    _gst_cd_subquery = select(gst_gg.gst_cd).filter(gst_gg.gg_cd == selected_gg.gg_cd).subquery()

    gst_list = (
        db.execute(
            select(gst).filter(gst.gst_cd.in_(select(_gst_cd_subquery))).filter(gst.gst_cd.in_(select(_gst_publicated)))
        )
        .scalars()
        .all()
    )

    # get all oe's that have access to this gg
    oe_best_list = (
        db.execute(select(oe).filter(oe.oe_cd.in_([gst.entity_oe_best.oe_cd for gst in gst_list])))
        .unique()
        .scalars()
        .all()
    )

    # get all oe's that have access to this gg
    oe_bron_list = (
        db.execute(select(oe).filter(oe.oe_cd.in_([gst.entity_oe_bron.oe_cd for gst in gst_list])))
        .unique()
        .scalars()
        .all()
    )

    _evtp_cd_subquery = (
        select(evtp_gst.evtp_cd).filter(evtp_gst.gst_cd.in_([gst.gst_cd for gst in gst_list])).subquery()
    )

    evtp_list = (
        db.execute(
            select(evtp_version)
            .distinct(evtp_version.evtp_cd)
            .filter(evtp_version.evtp_cd.in_(select(_evtp_cd_subquery)))
            # Note that we have to filter the publication status and current version again to prevent
            # that the query returns all only evtps that are publicated and current
            .filter(evtp_version.id_publicatiestatus.in_(PUBLICATION_RANGE))
            .filter(evtp_version.huidige_versie.in_(CURRENT_VERSION))
        )
        .unique()
        .scalars()
        .all()
    )

    # create proper response
    result = schemas.details.GgDetails(
        gg=selected_gg,  # type: ignore
        evtp=[schemas.EvtpVersion.model_validate(evtp_item) for evtp_item in evtp_list],
        oe_bron=oe_bron_list,  # type: ignore
        oe_best=oe_best_list,  # type: ignore
    )
    return result


def get_filtered(db: Session, gg_query: schemas.gg.GgQuery) -> schemas.gg.GgQueryResult:
    """
    Get list of Gg's based on search parameters
    Q1 - Queries all Parent Gg's matching the search queries, including all child Gg's
    Q2 - Queries all Child Gg's matching the search queries, grouped under their parent Gg's
    Returns: Concatenated list of Q1 + Q2 (in that order)
    """
    model_gg = models.gg.Gg
    model_gg_struct = models.gg.GgStruct

    grouped_children = search_parent_ggs(db, gg_query, model_gg)
    children_results = search_child_ggs(db, gg_query, model_gg)

    child_parent_pairs = create_child_parent_pairs(grouped_children, children_results)
    filtered_pairs = filter_orphaned_children(db, child_parent_pairs)

    parents = get_paginated_parents(db, gg_query, filtered_pairs, model_gg, model_gg_struct)

    unique_parents = set(pair.parent_cd for pair in filtered_pairs)
    unique_children = set(pair.child_cd for pair in filtered_pairs)

    return schemas.gg.GgQueryResult(
        result_gg=parents,
        total_count_koepel=len(unique_parents),
        total_count_underlying=len(unique_children),
    )


def search_parent_ggs(db: Session, gg_query: schemas.gg.GgQuery, model_gg) -> List[schemas.ChildParentPair]:
    if not gg_query.searchtext:
        return []

    filter_ilike, filter_synonyms, similarity_score = build_filters_gg(gg_query.searchtext, model_gg)
    where_clause = and_(model_gg.child_gg_struct.has(), or_(filter_ilike, filter_synonyms))

    parent_searchresult = db.scalars(select(model_gg).filter(where_clause).order_by(desc(similarity_score))).all()

    if not parent_searchresult:
        logging.info("Enter search - Ilike search with synonyms did not give any results for parent gegevens")
        searchtext = prep_search_for_query(gg_query.searchtext)
        filter_similarities = get_similarity_search_clause(searchtext, model_gg, suggestion_search=False)
        parent_searchresult = db.scalars(
            select(model_gg).filter(filter_similarities).order_by(desc(similarity_score))
        ).all()
        if parent_searchresult:
            logging.info(f"Enter-search - Similarity search query for parent gegevens: {gg_query.searchtext}")
        else:
            logging.info("Enter-search - Similarity search query did not give any results for parent gegevens")
    else:
        logging.info(f"Enter search - Ilike search with synonyms results for parent gegevens: {gg_query.searchtext}")

    return [
        schemas.ChildParentPair(parent_cd=item.gg_cd, child_cd=child.gg_cd)
        for item in parent_searchresult
        for child in item.child_gg_entity
    ]


def search_child_ggs(db: Session, gg_query: schemas.gg.GgQuery, model_gg):
    filter_ilike, filter_synonyms, similarity_score = build_filters_gg(gg_query.searchtext, model_gg)
    where_clause = and_(
        or_(filter_ilike, filter_synonyms), model_gg.parent_gg_entity.any(), model_gg.gst_gg_entity.has()
    )

    children_searchresult = (
        db.scalars(
            select(model_gg)
            .options(joinedload(model_gg.parent_gg_entity))
            .filter(where_clause)
            .order_by(similarity_score)
        )
        .unique()
        .all()
    )

    if not children_searchresult:
        logging.info("Enter search - Ilike search did not give any results for child gegevens")
        searchtext = prep_search_for_query(gg_query.searchtext)
        filter_similarities = get_similarity_search_clause(searchtext, model_gg, suggestion_search=False)
        children_searchresult = (
            db.scalars(select(model_gg).options(joinedload(model_gg.parent_gg_entity)).filter(filter_similarities))
            .unique()
            .all()
        )
        if children_searchresult:
            logging.info(f"Enter-search - Similarity search query for child gegevens: {gg_query.searchtext}")
        else:
            logging.info("Enter-search - Similarity search query did not give any results for child gegevens")
    else:
        logging.info(f"Enter search - Ilike search with synonyms results for child gegevens: {gg_query.searchtext}")

    return children_searchresult


def create_child_parent_pairs(
    grouped_children: List[schemas.ChildParentPair], children_searchresult
) -> List[schemas.ChildParentPair]:
    isolated_children = [
        schemas.ChildParentPair(parent_cd=parent.gg_cd, child_cd=item.gg_cd)
        for item in children_searchresult
        for parent in item.parent_gg_entity
    ]
    return grouped_children + isolated_children


def filter_orphaned_children(
    db: Session, child_parent_pairs: List[schemas.ChildParentPair]
) -> List[schemas.ChildParentPair]:
    valid_child_gg_cds = db.scalars(
        text(
            f"""
            SELECT gg.gg_cd
            FROM gg
            INNER JOIN gst_gg ON
                gg.gg_cd = gst_gg.gg_cd
                AND gst_gg.ts_end > {func.now()}
                AND gst_gg.ts_start < {func.now()}
            INNER JOIN evtp_gst ON
                gst_gg.gst_cd = evtp_gst.gst_cd
            INNER JOIN evtp_version ON
                evtp_gst.evtp_cd = evtp_version.evtp_cd
                AND evtp_version.id_publicatiestatus IN ({', '.join(map(repr, PUBLICATION_RANGE))})
                AND evtp_version.ts_start < evtp_gst.ts_end
                AND evtp_version.ts_end > evtp_gst.ts_start;
            """
        )
    ).all()

    return [pair for pair in child_parent_pairs if pair.child_cd in valid_child_gg_cds]


def get_paginated_parents(
    db: Session,
    gg_query: schemas.gg.GgQuery,
    child_parent_pairs: List[schemas.ChildParentPair],
    model_gg,
    model_gg_struct,
):
    result_range = ((gg_query.page - 1) * gg_query.limit, gg_query.page * gg_query.limit)
    parent_cds = sorted(set(pair.parent_cd for pair in child_parent_pairs))[result_range[0] : result_range[1]]

    if not parent_cds:
        return []

    id_ordering = case({_id: index for index, _id in enumerate(parent_cds)}, value=model_gg.gg_cd)

    q_parents = db.scalars(select(model_gg).filter(model_gg.gg_cd.in_(parent_cds)).order_by(id_ordering))

    parents = []
    for item in q_parents:
        q_children_cds = [pair.child_cd for pair in child_parent_pairs if pair.parent_cd == item.gg_cd]
        q_children = db.scalars(
            select(model_gg_struct).filter(
                model_gg_struct.gg_cd_sub.in_(q_children_cds),
                model_gg_struct.gg_cd_sup == item.gg_cd,
            )
        )

        children = list(q_children)
        parent = schemas.gg.ParentGg(
            gg_cd=item.gg_cd,
            omschrijving=item.omschrijving,
            omschrijving_uitgebreid=item.omschrijving_uitgebreid,
            child_gg_struct=children,
        )
        parents.append(parent)

    return parents


def get_search_suggestion(db: Session, search_query: str):
    model_gg = models.gg.Gg
    query_filters = []

    valid_child_gg_cds = db.scalars(
        text(
            f"""
            SELECT gg.gg_cd
            FROM gg
            JOIN gst_gg gsg ON
                gg.gg_cd = gsg.gg_cd
                AND gsg.ts_end > {func.now()}
                AND gsg.ts_start < {func.now()}
            JOIN evtp_gst eg ON
                gsg.gst_cd = eg.gst_cd
            JOIN evtp_version ev ON
                eg.evtp_cd = ev.evtp_cd
                AND ev.id_publicatiestatus IN ({', '.join(map(repr, PUBLICATION_RANGE))})
                AND ev.ts_start < eg.ts_end
                AND ev.ts_end > eg.ts_start;
            """
        )
    ).all()

    if search_query:
        filter_ilike = model_gg.omschrijving.ilike(f"%{search_query}%")
        filter_synonyms = model_gg.vector.op("@@")(func.websearch_to_tsquery("NLD", search_query))
        similarity_score = func.similarity(model_gg.omschrijving, search_query)

        query = (
            select(model_gg)
            .where(and_(*query_filters, or_(filter_ilike, filter_synonyms), model_gg.gg_cd.in_(valid_child_gg_cds)))
            .order_by(desc(similarity_score))
        )

        query_gg = db.execute(query).scalars().all()

        if not query_gg:
            logging.info("Suggestion search - ilike did not give any results for child gegevens")
            search_condition = get_similarity_search_clause(
                search_query, model=model_gg, suggestion_search=True, search_restricted=False
            )
            query_filters.append(search_condition)
            query = (
                select(model_gg, similarity_score)
                .where(and_(*query_filters, model_gg.gg_cd.in_(valid_child_gg_cds)))
                .order_by(desc(similarity_score))
            )
            query_gg = db.execute(query).scalars().all()
            if query_gg:
                logging.info(f"Suggestion-search - Similarity search query for gegevens for: {search_query}")
            else:
                logging.info("Suggestion-search - Similarity search did not give any results for gegevens")
        else:
            logging.info(
                f"Suggestion search - Ilike search with synonyms results for child gegevens for: {search_query}"
            )
    else:
        query = select(model_gg).where(and_(*query_filters))
        query_gg = db.execute(query).scalars().all()

    return schemas.common.SearchSuggestionsAllEntities(
        gg=[
            schemas.common.SearchSuggestion(title=query_object.omschrijving, upc=query_object.gg_upc, version=None)
            for query_object in query_gg
        ],
        evtp=[],
        oe=[],
    )
