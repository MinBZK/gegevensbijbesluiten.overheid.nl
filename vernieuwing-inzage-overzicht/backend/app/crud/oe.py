import logging
from typing import Sequence

from sqlalchemy import (
    and_,
    or_,
    select,
    text,
    true,
)
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql.expression import (
    case,
)

import app.models as models
import app.schemas as schemas
from app.core.config import (
    CURRENT_VERSION,
    PUBLICATION_RANGE,
)
from app.database.database import Base
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


def __gen_where_clause(oe_query: schemas.oe.OeQuery, selected_columns: list[str], model: Base):
    """
    Create a where clause based on the model to filter on search query
    """
    filters = []
    selected_filters = []
    if oe_query.searchtext:
        selected_filters.append({"key": "searchtext", "value": oe_query.searchtext})
        search_clauses = [
            col.ilike(f"%{oe_query.searchtext.lower()}%")
            for col in [c for c in model.__table__.columns if c.key in selected_columns]
        ]
        filters.append(or_(*search_clauses))
    where_clause = and_(true(), *filters)
    return where_clause


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

    # Apply filters and search queries to find parent_oe's and their children
    if oe_query.searchtext:
        parent_searchresult = (
            db.execute(
                select(models.oe.OeKoepel)
                .filter(models.oe.OeKoepel.child_oe_struct.has())
                .filter(__gen_where_clause(oe_query, ["titel", "omschrijving"], models.oe.OeKoepel))
            )
            .scalars()
            .all()
        )
        grouped_children = [
            [item.oe_koepel_cd, child.oe_cd] for item in parent_searchresult for child in item.child_entities
        ]
    else:
        grouped_children = []

    # Apply filters and search queries to find child_oe's
    children_searchresult = (
        db.execute(
            select(models.oe.Oe)
            .options(joinedload(models.oe.Oe.parent_entities))
            .filter(__gen_where_clause(oe_query, ["naam_officieel"], models.oe.Oe))
            .filter(models.oe.Oe.parent_oe_struct.has())
        )
        .unique()
        .scalars()
        .all()
    )

    # Match the children to their parents (oe_cd only)
    isolated_children = [
        [parent.oe_koepel_cd, item.oe_cd] for item in children_searchresult for parent in item.parent_entities
    ]

    # Concatenate the matched parents and the children
    child_parent_cds = list(grouped_children) + isolated_children  # type: ignore

    if not child_parent_cds:
        # No results found
        parents = []
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
                value=models.oe.OeKoepel.oe_koepel_cd,
            )
        else:
            id_ordering = None

        # Query parents in the desired order
        parents = []
        if id_ordering is not None:
            q_parents = db.scalars(
                select(models.oe.OeKoepel).filter(models.oe.OeKoepel.oe_koepel_cd.in_(parent_cds)).order_by(id_ordering)
            )

            for item in q_parents:
                q_children_cds = [
                    child_cd for parent_cd, child_cd in child_parent_cds_ranged if parent_cd == item.oe_koepel_cd
                ]

                q_children = db.scalars(
                    select(models.oe.OeKoepelOe).filter(
                        models.oe.OeKoepelOe.oe_cd.in_(q_children_cds),
                        models.oe.OeKoepelOe.oe_koepel_cd == item.oe_koepel_cd,
                    )
                )

                children = [child for child in q_children]
                parent = schemas.oe.OeKoepel(
                    titel=item.titel,
                    omschrijving=item.omschrijving,
                    child_oe_struct=children,
                )
                parents.append(parent)
        else:
            q_parents = []

    unique_parents = set(item[0] for item in child_parent_cds)
    unique_children = set([item[1] for item in child_parent_cds])

    response = schemas.oe.OeQueryResult(
        results=parents,
        total_count_koepel=len(unique_parents),
        total_count_underlying=len(unique_children),
    )
    return response
