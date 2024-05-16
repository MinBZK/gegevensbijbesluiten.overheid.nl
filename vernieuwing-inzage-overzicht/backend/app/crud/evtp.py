import csv
import io
import logging
from datetime import datetime
from urllib.parse import urlparse

import pandas as pd
from fastapi.exceptions import (
    HTTPException,
)
from fastapi.responses import (
    StreamingResponse,
)
from sqlalchemy import (
    and_,
    desc,
    func,
    or_,
    select,
)
from sqlalchemy.orm import (
    Session,
    joinedload,
)

import app.models as models
import app.schemas as schemas
from app.core.config import (
    CURRENT_VERSION,
    PUBLICATION_RANGE,
)
from app.schemas.oe import (
    OeByEvtp,
    OeByEvtpTotal,
)

# Setup logger
logger = logging.getLogger(__name__)


def get_count(
    db: Session,
):
    """
    Gets count of evtps.
    Returns: number of evtps
    """
    return db.scalar(
        select(func.count(models.EvtpVersion.evtp_cd)).filter(
            models.EvtpVersion.id_publicatiestatus.in_(PUBLICATION_RANGE)
        )
    )


def get_filtered(
    db: Session,
    evtp_query: schemas.evtp.EvtpQuery,
) -> schemas.evtp.EvtpQueryResult:
    """
    Gets event type with filtered organization
    Returns: schema of event type with organization joined and metadata
    """
    selected_columns = [
        "omschrijving",
        "evtp_nm",
        "aanleiding",
        "gebr_dl",
    ]

    filters = []
    selected_filters = []
    filters.append(models.EvtpVersion.id_publicatiestatus.in_(PUBLICATION_RANGE))
    filters.append(models.EvtpVersion.huidige_versie.in_(CURRENT_VERSION))

    if evtp_query.searchtext:
        selected_filters.append(
            {
                "key": "searchtext",
                "value": evtp_query.searchtext,
            }
        )

        search_clauses = []
        # Select columns to search in from the table
        columns = models.EvtpVersion.__table__.columns
        columns_filtered = [c for c in columns if c.key in selected_columns]
        for col in columns_filtered:
            search_clauses.append(col.ilike(f"%{evtp_query.searchtext.lower()}%"))
        filters.append(or_(*search_clauses))

    if evtp_query.organisation:
        selected_filters.append(
            {
                "key": "organisation",
                "value": evtp_query.organisation,
            }
        )
        filters.append(models.Oe.naam_spraakgbr == evtp_query.organisation)

    where_clause = and_(*filters)

    query_evtp = (
        db.execute(
            select(models.EvtpVersion)
            .options(joinedload(models.EvtpVersion.entity_oe_best))
            .join(models.Oe)
            .filter(where_clause)
            .offset((evtp_query.page - 1) * evtp_query.limit)
            .limit(evtp_query.limit)
            .order_by(models.EvtpVersion.evtp_nm)
        )
        .scalars()
        .all()
    )

    organisation_filter_data = (
        db.query(
            models.Oe.naam_spraakgbr.label("label"),
            models.Oe.naam_spraakgbr.label("key"),
            func.count(models.EvtpVersion.oe_best).label("count"),
        )
        .select_from(models.EvtpVersion)
        .join(
            models.Oe,
        )
        .filter(where_clause)
        .group_by(models.Oe.naam_spraakgbr)
        .order_by(models.Oe.naam_spraakgbr)
        .all()
    )

    # Constructs returning total count.
    total_count = db.execute(
        select(func.count(models.EvtpVersion.evtp_cd))
        .join(
            models.Oe,
        )
        .filter(where_clause)
    ).scalar_one()

    filter_data = schemas.filters.EvtpFilterData(
        organisation=[schemas.filters.FilterData.model_validate(o) for o in organisation_filter_data],
        onderwerp=[],
    )

    return schemas.evtp.EvtpQueryResult(
        results=[schemas.evtp.EvtpVersion.model_validate(obj=query_object) for query_object in query_evtp],
        total_count=total_count,
        filter_data=filter_data,
        selected_filters=[schemas.filters.SelectedFilters(**dict(s)) for s in selected_filters],
    )


def get_evtp_gg(
    evtp_upc: int,
    db: Session,
    version_nr: int | None = None,
) -> schemas.evtp.EvtpGg:
    """
    Gets the gg related to a specific evtp based on the latest version.
    Returns: evtp with nested gg object
    """

    query_object = (
        db.execute(
            select(models.EvtpVersion)
            .join(models.Evtp)
            .options(
                joinedload(models.EvtpVersion.entities_evtp_gst)
                .joinedload(models.EvtpGst.entities_gst_gg)
                .joinedload(models.GstGg.entity_gg_child)
                .joinedload(models.Gg.parent_gg_struct)
                .joinedload(models.GgStruct.parent_gg_entity)
                .joinedload(models.Gg.parent_gg_struct)
                .joinedload(models.GgStruct.child_entity),
                joinedload(models.EvtpVersion.entities_evtp_gst)
                .joinedload(models.EvtpGst.entity_gst)
                .joinedload(models.Gst.entity_oe_best),
                joinedload(models.EvtpVersion.entities_evtp_oe_com_type),
                joinedload(models.EvtpVersion.entities_evtp_ond).joinedload(models.EvtpOnd.entity_evtp),
                joinedload(models.EvtpVersion.entities_evtp_gst)
                .joinedload(models.EvtpGst.entities_gst_rge)
                .joinedload(models.GstRge.entity_rge),
                joinedload(models.EvtpVersion.entities_evtp_oe_com_type)
                .joinedload(models.EvtpOeComType.entity_oe_com_type)
                .joinedload(models.OeComType.entities_oe_com_type),
            )
            .where(
                and_(
                    models.EvtpVersion.id_publicatiestatus.in_(PUBLICATION_RANGE),
                    models.EvtpVersion.huidige_versie.in_(CURRENT_VERSION),
                    models.Evtp.evtp_upc == evtp_upc,
                    models.EvtpVersion.versie_nr == (version_nr or models.EvtpVersion.versie_nr),
                )
            )
        )
        .unique()
        .scalar()
    )

    if not query_object:
        raise HTTPException(404)

    gg = {}

    for gst in query_object.entities_evtp_gst:
        parent_entity_gg_omschrijving = [
            child.entity_gg_child.parent_gg_struct.parent_gg_entity.omschrijving for child in gst.entities_gst_gg
        ][0]
        parent_entity_gg_sort_key = [
            (
                # set sort value to 1000 unless evtp_sort_key or sort_key is defined.
                # evtp_sort_key can overrule sort_key
                child.entity_gg_child.parent_gg_struct.parent_gg_entity.evtp_sort_key.get(query_object.evtp_cd)
                if query_object.evtp_cd in child.entity_gg_child.parent_gg_struct.parent_gg_entity.evtp_sort_key.keys()
                else (
                    child.entity_gg_child.parent_gg_struct.parent_gg_entity.sort_key
                    if child.entity_gg_child.parent_gg_struct.parent_gg_entity.sort_key
                    else 1000
                )
            )
            for child in gst.entities_gst_gg
        ][0]

        if parent_entity_gg_omschrijving not in gg.keys():
            gg[parent_entity_gg_omschrijving] = []

        # Transform date to string
        gg[parent_entity_gg_omschrijving].append(
            {
                "gg_child": [
                    child.entity_gg_child.omschrijving
                    for child in sorted(
                        gst.entities_gst_gg,
                        key=lambda item: item.sort_key if item.sort_key else 1000,
                    )
                ],
                "oe_best_naamspraakgbr": gst.entity_gst.entity_oe_bron.naam_spraakgbr,
                "gst_cd": gst.gst_cd,
                "gst_upc": gst.entity_gst.gst_upc,
                "gg_parent_sort_key": parent_entity_gg_sort_key,
                "evtp_gst_sort_key": gst.sort_key if gst.sort_key else 1000,
            }
        )

        # Sort gegevensstromen within gegevensgroep
        gg[parent_entity_gg_omschrijving] = sorted(
            gg[parent_entity_gg_omschrijving],
            key=lambda item: item["evtp_gst_sort_key"],
        )

    gg_sort_keys = {key: value[0]["gg_parent_sort_key"] for key, value in gg.items()}

    return schemas.evtp.EvtpGg(
        besluit=schemas.evtp.Besluit(
            evtp_cd=query_object.evtp_cd,
            evtp_upc=query_object.evtp_upc,
            evtp_nm=query_object.evtp_nm,
            omschrijving=query_object.omschrijving,
            aanleiding=query_object.aanleiding,
            gebr_dl=query_object.gebr_dl,
            soort_besluit=query_object.soort_besluit,
            lidw_soort_besluit=query_object.lidw_soort_besluit,
            oe_lidw_sgebr=query_object.entity_oe_best.lidw_sgebr,
            oe_naam_spraakgbr=query_object.entity_oe_best.naam_spraakgbr,
            oe_naam_officieel=query_object.entity_oe_best.naam_officieel,
            ond=[evtp_ond.entity_ond.titel for evtp_ond in query_object.entities_evtp_ond],
        ),
        gegevensgroep={
            k: v
            for k, v in sorted(
                gg.items(),
                key=lambda item: gg_sort_keys[item[0]],
            )
        },
        besluit_communicatie=schemas.evtp.EvtpCommunication(
            oe_best_econtact=query_object.entity_oe_best.e_contact,
            evtp_oe_com_type=(
                [
                    schemas.evtp.EvtpOeComType(
                        omschrijving=evtp_oe_com_type.entity_oe_com_type.omschrijving,
                        link=evtp_oe_com_type.link,
                    )
                    for evtp_oe_com_type in query_object.entities_evtp_oe_com_type
                ]
                if query_object.entities_evtp_oe_com_type
                else None
            ),
            oe_best_internetdomein=query_object.entity_oe_best.internet_domein,
            evtp_oebest=query_object.entity_oe_best.naam_spraakgbr,
        ),
    )


def get_evtp_gst(
    evtp_upc: int,
    gst_upc: int,
    db: Session,
    version_nr: int | None = None,
) -> schemas.EvtpGgGst:
    """
    Gets the gst related to a specific evtp.
    Returns: Evtp with nested gst object
    """
    query_gst_cd = db.execute(select(models.Gst.gst_cd).filter(models.Gst.gst_upc == gst_upc)).scalar()

    if not query_gst_cd:
        raise HTTPException(404)

    query_object_evtp_gst = db.execute(
        select(
            models.EvtpGst,
            models.EvtpVersion,
        )
        .options(
            joinedload(models.EvtpGst.entities_gst_gg)
            .joinedload(models.GstGg.entity_gg_child)
            .joinedload(models.Gg.parent_gg_struct)
            .joinedload(models.GgStruct.parent_gg_entity)
            .joinedload(models.Gg.parent_gg_struct)
            .joinedload(models.GgStruct.child_entity),
            joinedload(models.EvtpGst.entities_gst_rge).joinedload(models.GstRge.entity_rge),
            joinedload(models.EvtpGst.entity_evtp_version),
            joinedload(models.EvtpVersion.entities_evtp_gst)
            .joinedload(models.EvtpGst.entity_gst)
            .joinedload(models.Gst.entity_oe_best),
            joinedload(models.EvtpVersion.entities_evtp_gst)
            .joinedload(models.EvtpGst.entity_gst)
            .joinedload(models.Gst.entities_gst_gstt)
            .joinedload(models.GstGstt.entity_gst_type),
        )
        .join(
            models.EvtpVersion,
            and_(
                models.EvtpVersion.evtp_cd == models.EvtpGst.evtp_cd,
                models.EvtpVersion.ts_start < models.EvtpGst.ts_end,
                models.EvtpVersion.ts_end > models.EvtpGst.ts_start,
            ),
        )
        .where(
            and_(
                models.EvtpVersion.id_publicatiestatus.in_(PUBLICATION_RANGE),
                models.EvtpVersion.huidige_versie.in_(CURRENT_VERSION),
                models.EvtpVersion.evtp_upc == evtp_upc,
                models.EvtpVersion.versie_nr == (version_nr or models.EvtpVersion.versie_nr),
                models.EvtpGst.gst_cd == query_gst_cd,
            )
        )
    ).scalar()

    if not query_object_evtp_gst:
        raise HTTPException(404)

    ibron_oe_naam_spraakgbr = (
        query_object_evtp_gst.entity_gst.entity_ibron.entity_oe.naam_spraakgbr
        if query_object_evtp_gst.entity_gst.entity_ibron
        else (
            query_object_evtp_gst.entity_gst.entity_oe_bron.entity_ibron.entity_oe.naam_spraakgbr
            if query_object_evtp_gst.entity_gst.entity_oe_bron.entity_ibron
            else None
        )
    )

    ibron_oe_econtact = (
        query_object_evtp_gst.entity_gst.entity_oe_bron.entity_ibron.entity_oe.e_contact
        if query_object_evtp_gst.entity_gst.entity_oe_bron.entity_ibron
        else None
    )

    return schemas.EvtpGgGst(
        besluit=schemas.Besluit(
            evtp_nm=query_object_evtp_gst.entity_evtp_version.evtp_nm,
            evtp_upc=query_object_evtp_gst.entity_evtp_version.evtp_upc,
        ),
        bron_organisatie=schemas.BronOrganisatie(
            header_oe_bron_naamofficieel=query_object_evtp_gst.entity_gst.entity_oe_bron.naam_officieel,
            oe_bron_lidwsgebr=query_object_evtp_gst.entity_gst.entity_oe_bron.lidw_sgebr or "",
            oe_bron_internetdomein=query_object_evtp_gst.entity_gst.entity_oe_bron.internet_domein,
            ibron_oe_lidwsgebr=(
                query_object_evtp_gst.entity_gst.entity_oe_bron.entity_ibron.entity_oe.lidw_sgebr or ""
                if query_object_evtp_gst.entity_gst.entity_oe_bron.entity_ibron
                else None
            ),
            ibron_oe_naam_officieel=(
                query_object_evtp_gst.entity_gst.entity_ibron.entity_oe.naam_officieel
                if query_object_evtp_gst.entity_gst.entity_ibron
                else (
                    query_object_evtp_gst.entity_gst.entity_oe_bron.entity_ibron.entity_oe.naam_officieel
                    if query_object_evtp_gst.entity_gst.entity_oe_bron.entity_ibron
                    else None
                )
            ),
            ibron_oe_naam_spraakgbr=ibron_oe_naam_spraakgbr,
            oe_bron_naampraakgebr=query_object_evtp_gst.entity_gst.entity_oe_bron.naam_spraakgbr,
            gsttype_gsttoms=[
                gst_type.entity_gst_type.gstt_oms for gst_type in query_object_evtp_gst.entity_gst.entities_gst_gstt
            ],
            ibron_oe_econtact=ibron_oe_econtact,
            gst_extlnkaut=(
                query_object_evtp_gst.entity_gst.ext_lnk_aut
                if urlparse(query_object_evtp_gst.entity_gst.ext_lnk_aut).hostname
                else None
            ),
        ),
        gegevensgroep_grondslag=schemas.GegevensgroepGrondslag(
            header_oe_best_naamofficieel=query_object_evtp_gst.entity_gst.entity_oe_best.naam_officieel,
            gg_child=[
                gg_child.entity_gg_child.omschrijving
                for gg_child in sorted(
                    query_object_evtp_gst.entities_gst_gg,
                    key=lambda item: item.sort_key if item.sort_key else 1000,
                )
            ],
            gg_parent=query_object_evtp_gst.entities_gst_gg[
                0
            ].entity_gg_child.parent_gg_struct.parent_gg_entity.omschrijving,
            gg_omschrijvinguitgebreid=[
                gg_child.entity_gg_child.omschrijving_uitgebreid
                for gg_child in sorted(
                    query_object_evtp_gst.entities_gst_gg,
                    key=lambda item: item.sort_key if item.sort_key else 1000,
                )
            ],
            oe_best_lidwsgebr=query_object_evtp_gst.entity_gst.entity_oe_best.lidw_sgebr or "",
            oe_best_naampraakgebr=query_object_evtp_gst.entity_gst.entity_oe_best.naam_spraakgbr,
            evtp_aanleiding=query_object_evtp_gst.entity_evtp_version.aanleiding,
            evtp_gst_conditie=query_object_evtp_gst.conditie,
            evtp_gebrdl=query_object_evtp_gst.entity_evtp_version.gebr_dl,
            rge=[
                schemas.RgeShort(
                    titel=rge.entity_rge.titel,
                    re_link=rge.entity_rge.re_link,
                )
                for rge in sorted(
                    query_object_evtp_gst.entities_gst_rge,
                    key=lambda item: item.sort_key if item.sort_key else 1000,
                )
            ],
        ),
    )


def download_evtp(
    db: Session,
) -> StreamingResponse:
    query_object = (
        db.execute(
            select(models.EvtpVersion)
            .filter(
                models.EvtpVersion.id_publicatiestatus.in_(PUBLICATION_RANGE),
            )
            .order_by(models.EvtpVersion.evtp_nm)
        )
        .scalars()
        .all()
    )

    data = [schemas.evtp.EvtpVersion.model_validate(r).model_dump() for r in query_object]
    df = pd.json_normalize(data)
    columns: list[str] = [str(c) for c in df.columns]
    relevant_columns = [
        c
        for c in columns
        if c
        not in [
            "evtp_cd",
            "user_nm",
            "notitie",
            "lidw_soort_besluit",
            "soort_besluit",
            "sort_key",
            "versie_nr",
        ]
    ]
    stream = io.BytesIO()
    df = df[relevant_columns].replace(r"\n", "", regex=True)
    df = df.rename(
        columns={
            "evtp_upc": "unieke_code",
            "evtp_nm": "naam_besluit",
            "gebr_dl": "gebruiksdoel",
            "entities_evtp_ond": "onderwerp",
            "entity_oe_best.naam_spraakgbr": "organisatie",
        }
    )
    df["onderwerp"] = df["onderwerp"].apply(lambda x: x[0]["entity_ond"]["titel"] if x else None)
    df.to_csv(
        stream,
        index=False,
        quoting=csv.QUOTE_ALL,
        encoding="utf-8-sig",
    )

    response = StreamingResponse(
        iter([stream.getvalue()]),
        media_type="text/csv",
    )
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"besluiten_dump_{timestamp}.csv"

    response.headers["Content-Encoding"] = "UTF-8"
    response.headers["Content-type"] = "text/csv; charset=UTF-8"
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"

    return response


def get_by_publicatiestatus_oe(
    db: Session,
):
    """
    Gets all oe by published evtps
    """
    results = db.execute(
        select(
            models.Oe.naam_officieel,
            func.count(models.EvtpVersion.id_publicatiestatus),
        )
        .join(models.Oe)
        .where(
            and_(
                models.EvtpVersion.id_publicatiestatus.in_(PUBLICATION_RANGE),
                models.EvtpVersion.huidige_versie.is_(True),
            )
        )
        .group_by(models.Oe.naam_officieel)
        .order_by(desc(func.count(models.EvtpVersion.id_publicatiestatus)))
    ).all()

    oe_by_evtp = [
        OeByEvtp(
            naam_officieel=naam,
            count=count,
        )
        for naam, count in results
    ]
    return OeByEvtpTotal(oe_by_evtp_total=oe_by_evtp)
