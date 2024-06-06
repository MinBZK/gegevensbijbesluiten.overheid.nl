import logging
from typing import Sequence

from sqlalchemy import (
    and_,
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
) -> Sequence[models.oe.Oe]:
    """Return all oe's"""
    return db.execute(select(models.oe.Oe)).scalars().all()


@timeit_once
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

    # gg_best
    _gst_cd_subquery = select(models.gst.Gst.gst_cd).filter(models.gst.Gst.oe_bron == selected_oe.oe_cd).subquery()
    gg_bron = (
        db.execute(
            select(models.gg.Gg)
            .distinct(models.gg.Gg.gg_cd)
            .join(models.gst.GstGg)
            .filter(models.gst.GstGg.gst_cd.in_(select(_gst_cd_subquery)))
        )
        .unique()
        .scalars()
        .all()
    )

    # gg_bron
    _gst_cd_subquery = select(models.gst.Gst.gst_cd).filter(models.gst.Gst.oe_best == selected_oe.oe_cd).subquery()
    gg_best = (
        db.execute(
            select(models.gg.Gg)
            .distinct(models.gg.Gg.gg_cd)
            .join(models.gst.GstGg)
            .filter(models.gst.GstGg.gst_cd.in_(select(_gst_cd_subquery)))
        )
        .unique()
        .scalars()
        .all()
    )

    response = schemas.details.OeDetails(
        oe=selected_oe,  # type: ignore
        evtpManaged=evtp_list,  # type: ignore
        ggManaged=gg_bron,  # type: ignore
        ggReceive=gg_best,  # type: ignore
    )
    return response


@timeit_once
def get_filtered(
    db: Session,
    oe_query: schemas.oe.OeQuery,
) -> schemas.oe.OeQueryResult:
    """
    Get list of Oe's based on search parameters
    Q1 - Queries all Parent Oe's matching the search queries, including all child Oe's
    Q2 - Queries all CHild Oe's matching the search queries, grouped under their parent Oe's
    Returns: Concatenated list of Q1 + Q2 (in that order)
    """
    selected_columns = ["naam_officieel"]
    filters = []
    selected_filters = []

    if oe_query.searchtext:
        selected_filters.append({"key": "searchtext", "value": oe_query.searchtext})
        search_clauses = [
            col.ilike(f"%{oe_query.searchtext.lower()}%")
            for col in [c for c in models.oe.Oe.__table__.columns if c.key in selected_columns]
        ]
        filters.append(or_(*search_clauses))

    where_clause = and_(true(), *filters)

    # Apply filters and search queries to find parent_oe's and their children
    if oe_query.searchtext:
        parent_searchresult = (
            db.execute(select(models.oe.Oe).filter(models.oe.Oe.child_oe_struct.has()).filter(where_clause))
            .scalars()
            .all()
        )
        grouped_children = [[item.oe_cd, child.oe_cd] for item in parent_searchresult for child in item.child_oe_entity]
    else:
        grouped_children = []

    # Apply filters and search queries to find child_oe's
    children_searchresult = (
        db.execute(select(models.oe.Oe.oe_cd).filter(models.oe.Oe.parent_entity.any()).filter(where_clause))
        .scalars()
        .all()
    )

    # Match the children to their parents (oe_cd only)
    if children_searchresult:
        isolated_children = db.execute(
            text(
                f"""
                SELECT parent_oe.oe_cd, child_oe.oe_cd
                FROM oe AS parent_oe
                JOIN oe_struct ON parent_oe.oe_cd = oe_struct.oe_cd_sup
                JOIN oe AS child_oe ON oe_struct.oe_cd_sub = child_oe.oe_cd
                WHERE child_oe.oe_cd IN ({', '.join(map(repr, children_searchresult))})
                ORDER BY parent_oe.oe_cd, child_oe.oe_cd;
                """
            )
        ).all()
    else:
        isolated_children = []

    # Concatenate the matched parents and the children
    child_parent_cds = list(grouped_children) + isolated_children  # type: ignore

    if not child_parent_cds:
        # No results found
        parents = []
        num_results = 0
    else:
        # Filter any child oe's without any published evtp's
        orphaned_children = (
            db.execute(
                text(
                    f"""
                SELECT oe.oe_cd
                FROM oe
                INNER JOIN evtp_version ON oe.oe_cd = evtp_version.oe_best
                AND evtp_version.id_publicatiestatus IN ({', '.join(map(repr, PUBLICATION_RANGE))});
                """
                )
            )
            .scalars()
            .all()
        )

        child_parent_cds = [
            (parent_cd, child_cd) for parent_cd, child_cd in child_parent_cds if child_cd in orphaned_children
        ]
        num_results = len(set(cp[0] for cp in child_parent_cds))

        # Clip the results to the desired limit and offset
        result_range = (
            (oe_query.page - 1) * oe_query.limit,
            oe_query.page * oe_query.limit,
        )
        parent_cds = sorted(set(cp[0] for cp in child_parent_cds))[result_range[0] : result_range[1]]
        child_parent_cds_ranged = [
            (parent_cd, child_cd) for parent_cd, child_cd in child_parent_cds if parent_cd in parent_cds
        ]

        # Reorder items to place parent_oe matches first
        if parent_cds:
            id_ordering = case(
                {_id: index for index, _id in enumerate(parent_cds)},
                value=models.oe.Oe.oe_cd,
            )
        else:
            id_ordering = None

        # Query parents in the desired order
        parents = []
        if id_ordering is not None:
            q_parents = db.scalars(
                select(models.oe.Oe).filter(models.oe.Oe.oe_cd.in_(parent_cds)).order_by(id_ordering)
            )

            for item in q_parents:
                q_children_cds = [
                    child_cd for parent_cd, child_cd in child_parent_cds_ranged if parent_cd == item.oe_cd
                ]

                q_children = db.scalars(
                    select(models.oe.OeStruct).filter(models.oe.OeStruct.oe_cd_sub.in_(q_children_cds))
                )

                parent = schemas.oe.ParentOe(
                    oe_upc=item.oe_upc,
                    naam_officieel=item.naam_officieel,
                    child_oe_struct=[child for child in q_children],  # type: ignore
                )
                parents.append(parent)
        else:
            q_parents = []

    response = schemas.oe.OeQueryResult(
        results=parents,
        total_count=num_results,
    )
    return response
