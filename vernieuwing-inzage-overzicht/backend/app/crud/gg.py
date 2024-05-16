import logging

import numpy as np
from sqlalchemy import and_, func, or_, select, text, true
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
) -> list[models.gg.Gg]:
    """Return all (child) gg's"""
    return (
        db.execute(
            select(models.Gg).filter(models.Gg.parent_gg_entity is not None).filter(models.Gg.gst_gg_entity is not None)
        )
        .scalars()
        .all()
    )


def get_one(db: Session, gg_cd: int) -> schemas.gg.ChildGg:
    gg = models.Gg
    res = db.execute(select(gg).filter(gg.gg_cd == gg_cd)).scalars().one()
    return res


def get_details(db: Session, gg_upc: int) -> schemas.details.GgDetails:
    """
    Get details of a single selected Gg
    """
    gg = models.Gg
    evtp = models.EvtpVersion
    gst_gg = models.GstGg
    evtp_gst = models.EvtpGst
    gst = models.Gst
    oe = models.Oe
    # ibron = models.Ibron

    # Fetch all connected gst's
    selected_gg = db.execute(select(gg).filter(gg.gg_upc == gg_upc)).scalars().one()

    _gst_publicated = (
        select(evtp_gst.gst_cd)
        .join(
            evtp,
            and_(
                evtp.evtp_cd == evtp_gst.evtp_cd,
                evtp.ts_start < evtp_gst.ts_end,
                evtp.ts_end > evtp_gst.ts_start,
                evtp.ts_end > func.now(),
                evtp.ts_start < func.now(),
            ),
        )
        .filter(evtp.id_publicatiestatus.in_(PUBLICATION_RANGE))
        .filter(evtp.huidige_versie.in_(CURRENT_VERSION))
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

    # get all registers for this gg
    # ibron_list = (
    #     db.execute(select(ibron).filter(ibron.ibron_cd.in_([gst.entity_oe_bron.ibron_cd for gst in gst_list])))
    #     .unique()
    #     .scalars()
    #     .all()
    # )

    _evtp_cd_subquery = (
        select(evtp_gst.evtp_cd).filter(evtp_gst.gst_cd.in_([gst.gst_cd for gst in gst_list])).subquery()
    )

    evtp_list = (
        db.execute(
            select(evtp)
            .distinct(evtp.evtp_cd)
            .filter(evtp.evtp_cd.in_(select(_evtp_cd_subquery)))
            # Note that we have to filter the publication status and current version again to prevent
            # that the query returns all only evtps that are publicated and current
            .filter(evtp.id_publicatiestatus.in_(PUBLICATION_RANGE))
            .filter(evtp.huidige_versie.in_(CURRENT_VERSION))
        )
        .unique()
        .scalars()
        .all()
    )

    # create proper response
    result = schemas.details.GgDetails(
        gg=selected_gg,
        evtp=evtp_list,
        # ibron=ibron_list,
        oe_bron=oe_bron_list,
        oe_best=oe_best_list,
    )
    # logging.info(ibron_list[0].oe_cd)
    # logging.info(oe_bron_list[0].oe_cd)

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
    Returns: Concatenated list of Q1 + Q2 (in that order)
    """
    selected_columns = ["omschrijving"]

    filters = []
    selected_filters = []

    if gg_query.searchtext:
        selected_filters.append(
            {
                "key": "searchtext",
                "value": gg_query.searchtext,
            }
        )

        search_clauses = []
        # Select columns to search in from the table
        columns = models.Gg.__table__.columns
        columns_filtered = [c for c in columns if c.key in selected_columns]
        for col in columns_filtered:
            search_clauses.append(col.ilike(f"%{gg_query.searchtext.lower()}%"))
        filters.append(or_(*search_clauses))
    where_clause = and_(true(), *filters)

    # --------------- Q1 query for parent gg's ---------------
    # apply the filters and searchqueries to find parent_gg's and generate a list of all its children
    # this query is not fast, so skip it when there is no searchquery
    if gg_query.searchtext:
        _parent_searchresult = (
            db.execute(select(models.Gg).filter(models.Gg.child_gg_struct.any()).filter(where_clause)).scalars().all()
        )
        grouped_children = np.array(
            [
                [
                    item.gg_cd,
                    child.gg_cd,
                ]
                for item in _parent_searchresult
                for child in item.child_gg_entity
            ]
        )
    else:
        grouped_children = np.array([])

    # --------------- Q2 query for child gg's ---------------
    children_searchresult = (
        db.execute(
            select(models.Gg.gg_cd)
            .filter(models.Gg.parent_gg_entity is not None)
            .filter(models.Gg.gst_gg_entity is not None)
            .filter(where_clause)
        )
        .scalars()
        .all()
    )

    # match the children to their parents (gg_cd only)
    if children_searchresult:
        isolated_children = np.array(
            db.execute(
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
        )
    else:
        isolated_children = np.array([[]])
    # Locatie asverstrooiing

    # --------------- combine and process Q1 + Q2 ---------------
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
        num_results = 0

    else:
        # Filter any child gg's without any publicated evtp's
        valid_child_gg_cds = np.array(
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
            ).all()
        ).flatten()
        child_parent_cds = child_parent_cds[np.isin(child_parent_cds[:, 1], valid_child_gg_cds.flatten())]
        num_results = len(np.unique(child_parent_cds[:, 0]))

    if num_results == 0:
        parents = []
    else:
        # clip the results to 6 parents per page
        result_range = (
            (gg_query.page - 1) * gg_query.limit,
            gg_query.page * gg_query.limit,
        )
        _parent_cds = np.unique(child_parent_cds[:, 0])[result_range[0] : result_range[1]]
        child_parent_cds_ranged = child_parent_cds[np.isin(child_parent_cds[:, 0], _parent_cds)]

        # reorder items to place parent_gg matches first
        indexes = np.unique(
            child_parent_cds_ranged[:, 0],
            return_index=True,
        )[1]
        parent_cd_ordened = [int(child_parent_cds_ranged[:, 0][index]) for index in sorted(indexes)]
        id_ordering = case(
            {_id: index for index, _id in enumerate(parent_cd_ordened)},
            value=models.Gg.gg_cd,
        )

        # query parents in proper order
        q_parents = (
            db.execute(
                select(models.Gg)
                .filter(models.Gg.gg_cd.in_(child_parent_cds_ranged[:, 0].tolist()))
                .order_by(id_ordering)
            )
            .scalars()
            .all()
        )

        # Generate response where parent gg's only have a partial list of child gg
        parents = []
        for item in q_parents:
            q_children_cds = child_parent_cds_ranged[child_parent_cds_ranged[:, 0] == item.gg_cd][:, 1].tolist()
            q_children = (
                db.execute(select(models.GgStruct).filter(models.GgStruct.gg_cd_sub.in_(q_children_cds)))
                .scalars()
                .all()
            )
            parent = schemas.gg.ParentGg(
                gg_cd=item.gg_cd,
                omschrijving=item.omschrijving,
                omschrijving_uitgebreid=item.omschrijving_uitgebreid,
                sort_key=item.sort_key,
                evtp_sort_key=None,
                child_gg_struct=q_children,
            )
            parents.append(parent)

    response = schemas.gg.GgQueryResult(
        results=parents,
        total_count=num_results,
        filter_data=schemas.filters.GgFilterData(
            organisation=[],
            onderwerp=[],
        ),  #  No filters availlable
        selected_filters=[schemas.filters.SelectedFilters(**dict(s)) for s in selected_filters],
    )
    return response
