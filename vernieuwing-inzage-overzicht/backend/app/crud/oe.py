import logging

import numpy as np
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
) -> list[models.oe.Oe]:
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

    selected_oe = db.execute(select(models.Oe).filter(models.Oe.oe_upc == oe_upc)).scalars().one()

    # evtp
    evtp_list = (
        db.execute(
            select(models.EvtpVersion)
            .distinct(models.EvtpVersion.evtp_cd)
            .filter(models.EvtpVersion.oe_best == selected_oe.oe_cd)
            .filter(models.EvtpVersion.id_publicatiestatus.in_(PUBLICATION_RANGE))
            .filter(models.EvtpVersion.huidige_versie.in_(CURRENT_VERSION))
        )
        .unique()
        .scalars()
        .all()
    )

    # gg_best
    _gst_cd_subquery = select(models.Gst.gst_cd).filter(models.Gst.oe_bron == selected_oe.oe_cd).subquery()
    gg_bron = (
        db.execute(
            select(models.Gg)
            .distinct(models.Gg.gg_cd)
            .join(models.GstGg)
            .filter(models.GstGg.gst_cd.in_(select(_gst_cd_subquery)))
        )
        .unique()
        .scalars()
        .all()
    )

    # gg_bron
    _gst_cd_subquery = select(models.Gst.gst_cd).filter(models.Gst.oe_best == selected_oe.oe_cd).subquery()
    gg_best = (
        db.execute(
            select(models.Gg)
            .distinct(models.Gg.gg_cd)
            .join(models.GstGg)
            .filter(models.GstGg.gst_cd.in_(select(_gst_cd_subquery)))
        )
        .unique()
        .scalars()
        .all()
    )

    response = schemas.details.OeDetails(
        oe=selected_oe,
        evtpManaged=evtp_list,
        ggManaged=gg_bron,
        ggReceive=gg_best,
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
        selected_filters.append(
            {
                "key": "searchtext",
                "value": oe_query.searchtext,
            }
        )

        search_clauses = []
        # Select columns to search in from the table
        columns = models.Oe.__table__.columns
        columns_filtered = [c for c in columns if c.key in selected_columns]
        for col in columns_filtered:
            search_clauses.append(col.ilike(f"%{oe_query.searchtext.lower()}%"))
        filters.append(or_(*search_clauses))
    where_clause = and_(true(), *filters)

    # apply the filters and searchqueries to find parent_oe's and generate a list of all its children
    # this query is not fast, so skip it when there is no searchquery
    if oe_query.searchtext:
        _parent_searchresult = (
            db.execute(select(models.Oe).filter(models.Oe.child_oe_struct.any()).filter(where_clause)).scalars().all()
        )
        grouped_children = np.array(
            [
                [
                    item.oe_cd,
                    child.oe_cd,
                ]
                for item in _parent_searchresult
                for child in item.child_oe_entity
            ]
        )
    else:
        grouped_children = np.array([])

    # apply the filters and searchqueries to find child_oe's
    children_searchresult = (
        db.execute(select(models.Oe.oe_cd).filter(models.Oe.parent_oe_entity is not None).filter(where_clause))
        .scalars()
        .all()
    )

    # match the children to their parents (oe_cd only)
    if children_searchresult:
        isolated_children = np.array(
            db.execute(
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
        )
    else:
        isolated_children = np.array([[]])
    # Locatie asverstrooiing

    # concatenate the matched parents and the children
    if not grouped_children.any():
        child_parent_cds = isolated_children
    elif not isolated_children.any():
        child_parent_cds = grouped_children
    else:
        child_parent_cds = np.concatenate(
            (
                np.array(grouped_children),
                isolated_children,
            )
        )
    if not child_parent_cds.any():
        # no results found
        parents = []
        num_results = 0
    else:
        # Filter any child oe's without any publicated evtp's
        orphaned_children = np.array(
            db.execute(
                text(
                    f"""
                        SELECT oe.oe_cd
                        FROM oe
                        INNER JOIN evtp_version ON oe.oe_cd = evtp_version.oe_best
                        AND evtp_version.id_publicatiestatus IN ({', '.join(map(repr, PUBLICATION_RANGE))});
                    """
                )
            ).all()
        ).flatten()

        child_parent_cds = child_parent_cds[
            np.isin(
                child_parent_cds[:, 1],
                orphaned_children.flatten(),
            )
        ]

        # clip the results to 6 parents per page
        result_range = (
            (oe_query.page - 1) * oe_query.limit,
            oe_query.page * oe_query.limit,
        )
        _parent_cds = np.unique(child_parent_cds[:, 0])[result_range[0] : result_range[1]]
        child_parent_cds_ranged = child_parent_cds[
            np.isin(
                child_parent_cds[:, 0],
                _parent_cds,
            )
        ]
        num_results = len(np.unique(child_parent_cds[:, 0]))

        # reorder items to place parent_oe matches first
        indexes = np.unique(
            child_parent_cds_ranged[:, 0],
            return_index=True,
        )[1]
        parent_cd_ordened = [int(child_parent_cds_ranged[:, 0][index]) for index in sorted(indexes)]
        id_ordering = case(
            {_id: index for index, _id in enumerate(parent_cd_ordened)},
            value=models.Oe.oe_cd,
        )

        # query parents in proper order
        q_parents = (
            db.execute(
                select(models.Oe)
                .filter(models.Oe.oe_cd.in_(child_parent_cds_ranged[:, 0].tolist()))
                .order_by(id_ordering)
            )
            .scalars()
            .all()
        )

        # Generate response where parent oe's only have a partial list of child oe
        parents = []
        for item in q_parents:
            q_children_cds = child_parent_cds_ranged[child_parent_cds_ranged[:, 0] == item.oe_cd][:, 1].tolist()
            q_children = (
                db.execute(select(models.OeStruct).filter(models.OeStruct.oe_cd_sub.in_(q_children_cds)))
                .scalars()
                .all()
            )
            parent = schemas.oe.ParentOe(
                oe_cd=item.oe_cd,
                oe_upc=item.oe_upc,
                naam_officieel=item.naam_officieel,
                naam_spraakgbr=item.naam_spraakgbr,
                child_oe_struct=q_children,
            )
            parents.append(parent)

    response = schemas.oe.OeQueryResult(
        results=parents,
        total_count=num_results,
        filter_data=schemas.filters.OeFilterData(
            organisation=[],
            onderwerp=[],
        ),  #  No filters availlable
        selected_filters=[schemas.filters.SelectedFilters(**dict(s)) for s in selected_filters],
    )
    return response
