import logging
from typing import Sequence

from sqlalchemy import (
    and_,
    func,
    or_,
    select,
    text,
    true,
)
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import (
    case,
)

import app.models as models
import app.schemas as schemas
from app.core.config import (
    CURRENT_VERSION,
    PUBLICATION_RANGE,
)
from app.utils.decorators import (
    timeit_once,
)

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
    # ibron = models.Ibron

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


@timeit_once
def get_filtered(
    db: Session,
    gg_query: schemas.gg.GgQuery,
) -> schemas.gg.GgQueryResult:
    """
    Get list of Gg's based on search parameters
    Q1 - Queries all Parent Gg's matching the search queries, including all child Gg's
    Q2 - Queries all Child Gg's matching the search queries, grouped under their parent Gg's
    Q2 - Queries all Child Gg's matching the search queries, grouped under their parent Gg's
    Returns: Concatenated list of Q1 + Q2 (in that order)
    """
    selected_columns = ["omschrijving"]
    filters = []
    selected_filters = []

    if gg_query.searchtext:
        selected_filters.append({"key": "searchtext", "value": gg_query.searchtext})
        search_clauses = [
            col.ilike(f"%{gg_query.searchtext.lower()}%")
            for col in [c for c in models.gg.Gg.__table__.columns if c.key in selected_columns]
        ]
        filters.append(or_(*search_clauses))

    where_clause = and_(true(), *filters)

    # --------------- Q1 query for parent gg's --------------- #
    # apply the filters and searchqueries to find parent_gg's and generate a list of all its children
    # this query is not fast, so skip it when there is no searchquery
    if gg_query.searchtext:
        parent_searchresult = (
            db.execute(select(models.gg.Gg).filter(models.gg.Gg.child_gg_struct.has()).filter(where_clause))
            .scalars()
            .all()
        )
        grouped_children = [[item.gg_cd, child.gg_cd] for item in parent_searchresult for child in item.child_gg_entity]
    else:
        grouped_children = []

    # --------------- Q2 query for child gg's ---------------
    children_searchresult = (
        db.execute(
            select(models.gg.Gg.gg_cd)
            .filter(models.gg.Gg.parent_gg_entity.any())
            .filter(models.gg.Gg.gst_gg_entity.has())
            .filter(where_clause)
        )
        .scalars()
        .all()
    )

    # Match the children to their parents (gg_cd only)
    if children_searchresult:
        isolated_children = db.execute(
            text(
                f"""
                SELECT parent_gg.gg_cd, child_gg.gg_cd
                FROM gg AS parent_gg
                JOIN gg_struct ON parent_gg.gg_cd = gg_struct.gg_cd_sup
                JOIN gg AS child_gg ON gg_struct.gg_cd_sub = child_gg.gg_cd
                WHERE child_gg.gg_cd IN ({', '.join(map(repr, children_searchresult))})
                ORDER BY parent_gg.gg_cd, child_gg.gg_cd;
                """
            )
        ).all()
    else:
        isolated_children = []

    # --------------- combine and process Q1 + Q2 --------------- #
    # Concatenate the matched parents and the children
    child_parent_cds = list(grouped_children) + isolated_children  # type: ignore

    if not child_parent_cds:
        # No results found
        parents = []
        num_results = 0

    else:
        # Filter any child gg's without any published evtp's
        valid_child_gg_cds = (
            db.execute(
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
            )
            .scalars()
            .all()
        )

        child_parent_cds = [
            (parent_cd, child_cd) for parent_cd, child_cd in child_parent_cds if child_cd in valid_child_gg_cds
        ]
        num_results = len(set(cp[0] for cp in child_parent_cds))

        # Clip the results to the desired limit and offset
        result_range = (
            (gg_query.page - 1) * gg_query.limit,
            gg_query.page * gg_query.limit,
        )
        parent_cds = sorted(set(cp[0] for cp in child_parent_cds))[result_range[0] : result_range[1]]
        child_parent_cds_ranged = [
            (parent_cd, child_cd) for parent_cd, child_cd in child_parent_cds if parent_cd in parent_cds
        ]

        # Reorder items to place parent_gg matches first
        if parent_cds:
            id_ordering = case(
                {_id: index for index, _id in enumerate(parent_cds)},
                value=models.gg.Gg.gg_cd,
            )
        else:
            id_ordering = None

        # Query parents in the desired order
        parents = []
        if id_ordering is not None:
            q_parents = db.scalars(
                select(models.gg.Gg).filter(models.gg.Gg.gg_cd.in_(parent_cds)).order_by(id_ordering)
            )

            for item in q_parents:
                q_children_cds = [
                    child_cd for parent_cd, child_cd in child_parent_cds_ranged if parent_cd == item.gg_cd
                ]

                q_children = db.scalars(
                    select(models.gg.GgStruct).filter(models.gg.GgStruct.gg_cd_sub.in_(q_children_cds))
                )

                parent = schemas.gg.ParentGg(
                    gg_cd=item.gg_cd,
                    omschrijving=item.omschrijving,
                    omschrijving_uitgebreid=item.omschrijving_uitgebreid,
                    child_gg_struct=[child for child in q_children],  # type: ignore
                )
                parents.append(parent)
        else:
            q_parents = []

    response = schemas.gg.GgQueryResult(
        results=parents,
        total_count=num_results,
    )
    return response
