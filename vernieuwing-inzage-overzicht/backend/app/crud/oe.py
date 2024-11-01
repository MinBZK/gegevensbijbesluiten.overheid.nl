import logging
from typing import List, Sequence

from sqlalchemy import and_, desc, func, or_, select, text
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql.expression import (
    case,
)

import app.models as models
import app.schemas as schemas
from app.core.config import CURRENT_VERSION, PUBLICATION_RANGE
from app.crud.tls_search import (
    build_filters_oe,
    build_filters_oe_koepel,
    get_similarity_search_clause,
    prep_search_for_query,
)

# Setup logger
logger = logging.getLogger(__name__)


def get_all(
    db: Session,
) -> Sequence[models.oe.Oe]:
    """Return all oe's"""
    return db.execute(select(models.oe.Oe)).scalars().all()


def get_details(
    db: Session,
    oe_upc: int,
) -> schemas.details.OeDetails:
    """
    Query all oe's and filter based on searchquery (if required)
    """
    model_evtp_version = models.evtp.EvtpVersion
    selected_oe = db.execute(select(models.oe.Oe).filter(models.oe.Oe.oe_upc == oe_upc)).scalars().one()

    # evtp
    evtp_list = (
        db.execute(
            select(model_evtp_version)
            .distinct(model_evtp_version.evtp_cd)
            .filter(model_evtp_version.oe_best == selected_oe.oe_cd)
            .filter(model_evtp_version.id_publicatiestatus.in_(PUBLICATION_RANGE))
            .filter(model_evtp_version.huidige_versie.in_(CURRENT_VERSION))
        )
        .unique()
        .scalars()
        .all()
    )

    response = schemas.details.OeDetails(
        oe=selected_oe,  # type: ignore
        evtpManaged=evtp_list,  # type: ignore
    )
    return response


def get_filtered(db: Session, oe_query: schemas.oe.OeQuery) -> schemas.oe.OeQueryResult:
    """
    Get list of Oe's based on search parameters
    Q1 - Queries all Parent Oe's matching the search queries, including all child Oe's
    Q2 - Queries all Child Oe's matching the search queries, grouped under their parent Oe's
    Returns: Concatenated list of Q1 + Q2 (in that order)
    """
    model_oe = models.oe.Oe
    model_oe_koepel = models.oe.OeKoepel
    model_oe_koepel_oe = models.oe.OeKoepelOe

    grouped_children = search_parent_oes(db, oe_query, model_oe_koepel)
    children_results = search_child_oes(db, oe_query, model_oe)

    child_parent_pairs = create_child_parent_pairs(grouped_children, children_results)
    filtered_pairs = filter_orphaned_children(db, child_parent_pairs)

    parents = get_paginated_parents(db, oe_query, filtered_pairs, model_oe_koepel, model_oe_koepel_oe)

    unique_parents = set(pair.parent_cd for pair in filtered_pairs)
    unique_children = set(pair.child_cd for pair in filtered_pairs)

    return schemas.oe.OeQueryResult(
        result_oe=parents,
        total_count_koepel=len(unique_parents),
        total_count_underlying=len(unique_children),
    )


def search_parent_oes(db: Session, oe_query: schemas.oe.OeQuery, model_oe_koepel) -> List[schemas.ChildParentPair]:
    if not oe_query.searchtext:
        return []

    filter_ilike, filter_synonyms, similarity_score = build_filters_oe_koepel(oe_query.searchtext, model_oe_koepel)
    where_clause = and_(model_oe_koepel.child_oe_struct.has(), or_(filter_ilike, filter_synonyms))

    parent_searchresult = db.scalars(
        select(model_oe_koepel).filter(where_clause).order_by(desc(similarity_score))
    ).all()

    if not parent_searchresult:
        logging.info("Enter search - Ilike search with synonyms did not give any results for parent organisaties")
        searchtext = prep_search_for_query(oe_query.searchtext)
        filter_similarities = get_similarity_search_clause(searchtext, model_oe_koepel, suggestion_search=False)
        parent_searchresult = db.scalars(select(model_oe_koepel).filter(filter_similarities)).all()
        if parent_searchresult:
            logging.info(f"Enter-search - Similarity search query for parent organisaties: {oe_query.searchtext}")
        else:
            logging.info("Enter-search - Similarity search query did not give any results for parent organisaties")
    else:
        logging.info(
            f"Enter search - Ilike search with synonyms results for parent organisaties: {oe_query.searchtext}"
        )

    return [
        schemas.ChildParentPair(parent_cd=item.oe_koepel_cd, child_cd=child.oe_cd)
        for item in parent_searchresult
        for child in item.child_entities
    ]


def search_child_oes(db: Session, oe_query: schemas.oe.OeQuery, model_oe):
    filter_ilike, filter_synonyms, similarity_score = build_filters_oe(oe_query.searchtext, model_oe)
    where_clause = and_(or_(*filter_ilike, filter_synonyms), model_oe.parent_oe_struct.has())

    children_searchresult = (
        db.scalars(
            select(model_oe)
            .options(joinedload(model_oe.parent_entities))
            .filter(where_clause)
            .order_by(desc(similarity_score))
        )
        .unique()
        .all()
    )

    if not children_searchresult:
        logging.info("Enter search - Ilike search did not give any results for child organisaties")
        searchtext = prep_search_for_query(oe_query.searchtext)
        filter_similarities = get_similarity_search_clause(searchtext, model_oe, suggestion_search=False)
        children_searchresult = (
            db.scalars(select(model_oe).options(joinedload(model_oe.parent_entities)).filter(filter_similarities))
            .unique()
            .all()
        )
        if children_searchresult:
            logging.info(f"Enter-search - Similarity search query for child organisaties: {oe_query.searchtext}")
        else:
            logging.info("Enter-search - Similarity search query did not give any results for child organisaties")
    else:
        logging.info(f"Enter search - Ilike search with synonyms results for child organisaties: {oe_query.searchtext}")

    return children_searchresult


def create_child_parent_pairs(
    grouped_children: List[schemas.ChildParentPair], children_searchresult
) -> List[schemas.ChildParentPair]:
    isolated_children = [
        schemas.ChildParentPair(parent_cd=parent.oe_koepel_cd, child_cd=item.oe_cd)
        for item in children_searchresult
        for parent in item.parent_entities
    ]
    return grouped_children + isolated_children


def filter_orphaned_children(
    db: Session, child_parent_pairs: List[schemas.ChildParentPair]
) -> List[schemas.ChildParentPair]:
    orphaned_children = db.scalars(
        text(
            f"""
            SELECT oe.oe_cd
            FROM oe
            JOIN evtp_version ev ON oe.oe_cd = ev.oe_best
            AND ev.id_publicatiestatus IN ({', '.join(map(repr, PUBLICATION_RANGE))});
            """
        )
    ).all()

    return [pair for pair in child_parent_pairs if pair.child_cd in orphaned_children]


def get_paginated_parents(
    db: Session,
    oe_query: schemas.oe.OeQuery,
    child_parent_pairs: List[schemas.ChildParentPair],
    model_oe_koepel,
    model_oe_koepel_oe,
):
    result_range = ((oe_query.page - 1) * oe_query.limit, oe_query.page * oe_query.limit)
    parent_cds = sorted(set(pair.parent_cd for pair in child_parent_pairs))[result_range[0] : result_range[1]]

    if not parent_cds:
        return []

    id_ordering = case({_id: index for index, _id in enumerate(parent_cds)}, value=model_oe_koepel.oe_koepel_cd)

    q_parents = db.scalars(
        select(model_oe_koepel).filter(model_oe_koepel.oe_koepel_cd.in_(parent_cds)).order_by(id_ordering)
    )

    parents = []
    for item in q_parents:
        q_children_cds = [pair.child_cd for pair in child_parent_pairs if pair.parent_cd == item.oe_koepel_cd]
        q_children = db.scalars(
            select(model_oe_koepel_oe).filter(
                model_oe_koepel_oe.oe_cd.in_(q_children_cds),
                model_oe_koepel_oe.oe_koepel_cd == item.oe_koepel_cd,
            )
        )

        children = list(q_children)
        parent = schemas.oe.OeKoepel(
            titel=item.titel,
            omschrijving=item.omschrijving,
            child_oe_struct=children,
        )
        parents.append(parent)

    return parents


def get_search_suggestion(db: Session, search_query: str):
    model_oe = models.oe.Oe
    query_filters = []

    valid_oes = db.scalars(
        text(
            f"""
            SELECT oe.oe_cd
            FROM oe
            JOIN evtp_version ev ON
                ev.oe_best = oe.oe_cd
                AND ev.id_publicatiestatus IN ({', '.join(map(repr, PUBLICATION_RANGE))});
            """
        )
    ).all()

    if search_query:
        filter_ilike = model_oe.naam_officieel.ilike(f"%{search_query}%")
        filter_synonyms = model_oe.vector.op("@@")(func.websearch_to_tsquery("NLD", search_query))
        similarity_score = func.similarity(model_oe.naam_officieel, search_query)

        query = (
            select(model_oe)
            .where(and_(*query_filters, or_(filter_ilike, filter_synonyms), model_oe.oe_cd.in_(valid_oes)))
            .order_by(desc(similarity_score))
        )

        query_oe = db.execute(query).scalars().all()

        if not query_oe:
            logger.info("Suggestion search - ilike did not give any results for child organisaties")
            search_condition = get_similarity_search_clause(
                search_query, model=model_oe, suggestion_search=True, search_restricted=False
            )
            query_filters.append(search_condition)
            query = (
                select(model_oe, similarity_score)
                .where(and_(*query_filters, model_oe.oe_cd.in_(valid_oes)))
                .order_by(desc(similarity_score))
            )
            query_oe = db.execute(query).scalars().all()
            if query_oe:
                logging.info(f"Suggestion-search - Similarity search query for child organisaties for: {search_query}")
            else:
                logging.info("Suggestion-search - Similarity search did not give any results for child organisaties")
        else:
            logging.info(
                f"Suggestion search - Ilike search with synonyms results for child organisaties for : {search_query}"
            )
    else:
        query = select(model_oe).where(and_(*query_filters))
        query_oe = db.execute(query).scalars().all()

    return schemas.common.SearchSuggestionsAllEntities(
        gg=[],
        evtp=[],
        oe=[
            schemas.common.SearchSuggestion(title=query_object.naam_officieel, upc=query_object.oe_upc, version=None)
            for query_object in query_oe
        ],
    )
