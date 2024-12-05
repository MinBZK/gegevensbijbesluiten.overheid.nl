import csv
import io
import logging
from datetime import datetime

import pandas as pd
from fastapi.exceptions import HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import and_, desc, func, or_, select
from sqlalchemy.orm import Session, joinedload

import app.models as models
import app.schemas as schemas
from app.core.config import CURRENT_VERSION, PUBLICATION_RANGE
from app.crud.tls_search import get_similarity_search_clause, get_web_search_clause, prep_search_for_query
from app.schemas.oe import OeByEvtp, OeByEvtpTotal

logger = logging.getLogger(__name__)


def get_base_query_filters():
    return [
        models.evtp.EvtpVersion.id_publicatiestatus.in_(PUBLICATION_RANGE),
        models.evtp.EvtpVersion.huidige_versie.in_(CURRENT_VERSION),
    ]


def get_count(db: Session):
    base_filters = get_base_query_filters()
    return db.scalar(select(func.count(models.evtp.EvtpVersion.evtp_cd)).filter(and_(*base_filters)))


def build_filters(evtp_query: schemas.evtp.EvtpQuery, model_evtp_version):
    search_query = prep_search_for_query(evtp_query.searchtext)
    filters = []
    base_filters = get_base_query_filters()
    filters.extend(base_filters)
    selected_filters = []
    filter_ilike = []
    filter_synonyms = []
    similarity_score = ""

    if search_query:
        selected_filters.append({"key": "searchtext", "value": search_query})
        filter_ilike.append(model_evtp_version.evtp_nm.ilike(f"%{search_query}%"))
        filter_ilike.append(model_evtp_version.gebr_dl.ilike(f"%{search_query}%"))
        filter_ilike.append(model_evtp_version.aanleiding.ilike(f"%{search_query}%"))
        filter_synonyms.append(get_web_search_clause(search_query, model_evtp_version))
        similarity_score = func.similarity(model_evtp_version.evtp_nm, search_query)

    if evtp_query.organisation:
        selected_filters.append({"key": "organisation", "value": evtp_query.organisation})
        filters.append(models.oe.Oe.naam_spraakgbr == evtp_query.organisation)

    return filters, selected_filters, filter_ilike, filter_synonyms, similarity_score


def execute_query(db: Session, where_clause, evtp_query, similarity_score):
    model_evtp_version = models.evtp.EvtpVersion
    if similarity_score != "":
        return (
            db.execute(
                select(model_evtp_version)
                .options(joinedload(model_evtp_version.entity_oe_best))
                .join(models.oe.Oe)
                .filter(where_clause)
                .offset((evtp_query.page - 1) * evtp_query.limit)
                .limit(evtp_query.limit)
                .order_by(desc(similarity_score))
            )
            .scalars()
            .all()
        )
    else:
        return (
            db.execute(
                select(model_evtp_version)
                .options(joinedload(model_evtp_version.entity_oe_best))
                .join(models.oe.Oe)
                .filter(where_clause)
                .offset((evtp_query.page - 1) * evtp_query.limit)
                .limit(evtp_query.limit)
                .order_by(model_evtp_version.evtp_nm)
            )
            .scalars()
            .all()
        )


def fetch_organisation_filter_data(db: Session, model_evtp_version, where_clause):
    return (
        db.execute(
            select(
                models.oe.Oe.naam_spraakgbr.label("label"),
                models.oe.Oe.naam_spraakgbr.label("key"),
                func.count(model_evtp_version.oe_best).label("count"),
            )
            .select_from(model_evtp_version)
            .join(models.oe.Oe)
            .where(where_clause)
            .group_by(models.oe.Oe.naam_spraakgbr)
            .order_by(func.lower(models.oe.Oe.naam_spraakgbr))
        )
        .mappings()
        .all()
    )


def get_total_count(db: Session, model_evtp_version, where_clause):
    return db.execute(
        select(func.count(model_evtp_version.evtp_cd)).join(models.oe.Oe).filter(where_clause)
    ).scalar_one()


def fetch_and_format_organisation_filter_data(db: Session, model_evtp_version, where_clause):
    organisation_filter_data = fetch_organisation_filter_data(db, model_evtp_version, where_clause)
    filter_data = schemas.filters.EvtpFilterData(
        organisation=[schemas.filters.FilterData.model_validate(o) for o in organisation_filter_data],
    )
    return filter_data


def get_filtered(db: Session, evtp_query: schemas.evtp.EvtpQuery) -> schemas.evtp.EvtpQueryResult:
    # Ilike-search with synonyms
    model_evtp_version = models.evtp.EvtpVersion
    filters, selected_filters, filter_ilike, filter_synonyms, similarity_score = build_filters(
        evtp_query, model_evtp_version
    )
    where_clause = and_(*filters, or_(*filter_ilike, *filter_synonyms))

    query_evtp = execute_query(db, where_clause, evtp_query, similarity_score)
    total_count = get_total_count(db, model_evtp_version, where_clause)
    if query_evtp:
        logging.info(f"Enter search - Ilike search with synonyms for besluiten for: {evtp_query.searchtext}")

    organisation_filter_data = fetch_and_format_organisation_filter_data(
        db=db, model_evtp_version=model_evtp_version, where_clause=where_clause
    )

    total_results = schemas.evtp.EvtpQueryResult(
        result_evtp=[schemas.evtp.EvtpVersion.model_validate(obj=query_object) for query_object in query_evtp],
        total_count=total_count,
        filter_data=organisation_filter_data,
        selected_filters=[schemas.filters.SelectedFilters(**dict(s)) for s in selected_filters],
    )

    # Similarity search
    if not total_results.result_evtp and evtp_query.searchtext:
        logging.info("Enter search - ilike did not give any results for besluiten")
        searchtext = prep_search_for_query(evtp_query.searchtext)
        filters[-1] = get_similarity_search_clause(searchtext, model_evtp_version, suggestion_search=False)
        where_clause = and_(*filters)
        query = (
            select(model_evtp_version)
            .where(where_clause)
            .offset((evtp_query.page - 1) * evtp_query.limit)
            .limit(evtp_query.limit)
        )
        query_evtp = db.execute(query).scalars().all()
        total_count = get_total_count(db, model_evtp_version, where_clause)
        logging.info(f"Enter-search - Similarity search query for besluiten for: {evtp_query.searchtext}")

        organisation_filter_data = fetch_and_format_organisation_filter_data(
            db=db, model_evtp_version=model_evtp_version, where_clause=where_clause
        )

        total_results = schemas.evtp.EvtpQueryResult(
            result_evtp=[schemas.evtp.EvtpVersion.model_validate(obj=query_object) for query_object in query_evtp],
            total_count=total_count,
            filter_data=organisation_filter_data,
            selected_filters=[schemas.filters.SelectedFilters(**dict(s)) for s in selected_filters],
        )

    return total_results


def get_evtp_gg(evtp_upc: int, db: Session, version_nr: int | None = None) -> schemas.evtp.EvtpGg:
    model_evtp_version = models.evtp.EvtpVersion
    query_object = (
        db.execute(
            select(model_evtp_version)
            .join(models.evtp.Evtp)
            .options(
                joinedload(model_evtp_version.entities_evtp_gst)
                .joinedload(models.evtp.EvtpGst.entities_gst_gg)
                .joinedload(models.gst.GstGg.entity_gg_child)
                .joinedload(models.gg.Gg.parent_gg_struct)
                .joinedload(models.gg.GgStruct.parent_entity)
                .joinedload(models.gg.Gg.parent_gg_struct)
                .joinedload(models.gg.GgStruct.child_entity),
                joinedload(model_evtp_version.entities_evtp_gst)
                .joinedload(models.evtp.EvtpGst.entity_gst)
                .joinedload(models.gst.Gst.entity_oe_best),
                joinedload(model_evtp_version.entities_evtp_oe_com_type),
                joinedload(model_evtp_version.entities_evtp_ond).joinedload(models.ond.EvtpOnd.entity_evtp_version),
                joinedload(model_evtp_version.entities_evtp_gst)
                .joinedload(models.evtp.EvtpGst.entities_gst_rge)
                .joinedload(models.gst.GstRge.entity_rge),
            )
            .where(
                and_(
                    model_evtp_version.id_publicatiestatus.in_(PUBLICATION_RANGE),
                    model_evtp_version.huidige_versie.in_(CURRENT_VERSION),
                    model_evtp_version.evtp_upc == evtp_upc,
                    model_evtp_version.versie_nr == (version_nr or model_evtp_version.versie_nr),
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
        parent_entity_gg_omschrijving = gst.entities_gst_gg[
            0
        ].entity_gg_child.parent_gg_struct.parent_entity.omschrijving
        parent_entity_gg_sort_key = gst.entities_gst_gg[
            0
        ].entity_gg_child.parent_gg_struct.parent_entity.evtp_sort_key.get(
            query_object.evtp_cd, gst.entities_gst_gg[0].entity_gg_child.parent_gg_struct.parent_entity.sort_key or 1000
        )

        if parent_entity_gg_omschrijving not in gg:
            gg[parent_entity_gg_omschrijving] = []

        gg[parent_entity_gg_omschrijving].append(
            {
                "gg_child": [
                    child.entity_gg_child.omschrijving
                    for child in sorted(
                        gst.entities_gst_gg, key=lambda item: (item.sort_key or 1000, item.entity_gg_child.omschrijving)
                    )
                ],
                "oe_best_naamspraakgbr": gst.entity_gst.entity_oe_bron.naam_spraakgbr,
                "gst_cd": gst.gst_cd,
                "gst_upc": gst.entity_gst.gst_upc,
                "gg_parent_sort_key": parent_entity_gg_sort_key,
                "evtp_gst_sort_key": gst.sort_key or 1000,
            }
        )

        gg[parent_entity_gg_omschrijving].sort(key=lambda item: item["evtp_gst_sort_key"])

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
            entity_omg=query_object.entity_omg,  # type: ignore
        ),
        gegevensgroep=dict(sorted(gg.items(), key=lambda item: gg_sort_keys[item[0]])),
        besluit_communicatie=schemas.evtp.EvtpCommunication(
            evtp_oe_com_type=[
                schemas.evtp.EvtpOeComType(
                    omschrijving=evtp_oe_com_type.entity_oe_com_type.omschrijving,
                    link=evtp_oe_com_type.link,
                )
                for evtp_oe_com_type in query_object.entities_evtp_oe_com_type
            ]
            if query_object.entities_evtp_oe_com_type
            else None,
            oe_best_internetdomein=query_object.entity_oe_best.internet_domein,
            evtp_oebest=query_object.entity_oe_best.naam_spraakgbr,
            overige_informatie=query_object.overige_informatie,
            overige_informatie_link=query_object.overige_informatie_link,
        ),
    )


def get_evtp_gst(evtp_upc: int, gst_upc: int, db: Session, version_nr: int | None = None) -> schemas.EvtpGgGst:
    model_evtp_version = models.evtp.EvtpVersion
    query_gst_cd = db.execute(select(models.gst.Gst.gst_cd).filter(models.gst.Gst.gst_upc == gst_upc)).scalar()

    if not query_gst_cd:
        raise HTTPException(404)

    query_object_evtp_gst = db.execute(
        select(models.evtp.EvtpGst, model_evtp_version)
        .options(
            joinedload(models.evtp.EvtpGst.entities_gst_gg)
            .joinedload(models.gst.GstGg.entity_gg_child)
            .joinedload(models.gg.Gg.parent_gg_struct)
            .joinedload(models.gg.GgStruct.parent_entity)
            .joinedload(models.gg.Gg.parent_gg_struct)
            .joinedload(models.gg.GgStruct.child_entity),
            joinedload(models.evtp.EvtpGst.entities_gst_rge).joinedload(models.gst.GstRge.entity_rge),
            joinedload(models.evtp.EvtpGst.entity_evtp_version),
            joinedload(model_evtp_version.entities_evtp_gst)
            .joinedload(models.evtp.EvtpGst.entity_gst)
            .joinedload(models.gst.Gst.entity_oe_best),
            joinedload(model_evtp_version.entities_evtp_gst).joinedload(models.evtp.EvtpGst.entity_gst),
            joinedload(model_evtp_version.entities_evtp_oe_com_type),
            joinedload(model_evtp_version.entities_evtp_gst)
            .joinedload(models.evtp.EvtpGst.entities_gst_gstt)
            .joinedload(models.gst.GstGstt.entity_gst_type),
        )
        .join(
            model_evtp_version,
            and_(
                model_evtp_version.evtp_cd == models.evtp.EvtpGst.evtp_cd,
                model_evtp_version.ts_start < models.evtp.EvtpGst.ts_end,
                model_evtp_version.ts_end > models.evtp.EvtpGst.ts_start,
            ),
        )
        .where(
            and_(
                model_evtp_version.id_publicatiestatus.in_(PUBLICATION_RANGE),
                model_evtp_version.huidige_versie.in_(CURRENT_VERSION),
                model_evtp_version.evtp_upc == evtp_upc,
                model_evtp_version.versie_nr == (version_nr or model_evtp_version.versie_nr),
                models.evtp.EvtpGst.gst_cd == query_gst_cd,
            )
        )
    ).scalar()

    if not query_object_evtp_gst:
        raise HTTPException(404)

    ibron_oe_naam_officieel = (
        query_object_evtp_gst.entity_gst.entity_ibron.entity_oe.naam_officieel
        if query_object_evtp_gst.entity_gst.entity_ibron
        else None
    )

    return schemas.EvtpGgGst(
        besluit=schemas.Besluit(
            evtp_nm=query_object_evtp_gst.entity_evtp_version.evtp_nm,
            evtp_upc=query_object_evtp_gst.entity_evtp_version.evtp_upc,
        ),
        bron_organisatie=schemas.BronOrganisatie(
            header_oe_bron_naamofficieel=query_object_evtp_gst.entity_gst.entity_oe_bron.naam_officieel,
            oe_bron_naampraakgebr=query_object_evtp_gst.entity_gst.entity_oe_bron.naam_spraakgbr,
            oe_bron_lidwsgebr=query_object_evtp_gst.entity_gst.entity_oe_bron.lidw_sgebr or "",
            oe_bron_internetdomein=query_object_evtp_gst.entity_gst.entity_oe_bron.internet_domein,
            ibron_oe_naam_officieel=ibron_oe_naam_officieel,
            ibron_oe_lidw=query_object_evtp_gst.entity_gst.entity_ibron.entity_oe.lidw_sgebr
            if query_object_evtp_gst.entity_gst.entity_ibron
            else None,
            ibron_titel=query_object_evtp_gst.entity_gst.entity_ibron.titel
            if query_object_evtp_gst.entity_gst.entity_ibron
            else None,
            ibron_lidw=query_object_evtp_gst.entity_gst.entity_ibron.lidw
            if query_object_evtp_gst.entity_gst.entity_ibron
            else None,
            ibron_link=query_object_evtp_gst.entity_gst.entity_ibron.link
            if query_object_evtp_gst.entity_gst.entity_ibron
            else None,
            gsttype_gsttoms=[gst_type.entity_gst_type.gstt_oms for gst_type in query_object_evtp_gst.entities_gst_gstt],
            gst_extlnkaut=query_object_evtp_gst.entity_gst.ext_lnk_aut,
        ),
        gegevensgroep_grondslag=schemas.GegevensgroepGrondslag(
            header_oe_best_naamofficieel=query_object_evtp_gst.entity_gst.entity_oe_best.naam_officieel,
            gg_child=[
                schemas.GgChild(
                    gg_cd=gg_child.entity_gg_child.gg_cd,
                    omschrijving=gg_child.entity_gg_child.omschrijving,
                    gg_upc=gg_child.entity_gg_child.gg_upc,
                )
                for gg_child in sorted(
                    query_object_evtp_gst.entities_gst_gg,
                    key=lambda item: (item.sort_key or 1000, item.entity_gg_child.omschrijving),
                )
            ],
            gg_parent=query_object_evtp_gst.entities_gst_gg[
                0
            ].entity_gg_child.parent_gg_struct.parent_entity.omschrijving,
            gg_omschrijvinguitgebreid=[
                gg_child.entity_gg_child.omschrijving_uitgebreid
                for gg_child in sorted(
                    query_object_evtp_gst.entities_gst_gg,
                    key=lambda item: (item.sort_key or 1000, item.entity_gg_child.omschrijving),
                )
            ],
            oe_best_lidwsgebr=query_object_evtp_gst.entity_gst.entity_oe_best.lidw_sgebr or "",
            oe_best_naampraakgebr=query_object_evtp_gst.entity_gst.entity_oe_best.naam_spraakgbr,
            evtp_aanleiding=query_object_evtp_gst.entity_evtp_version.aanleiding,
            gst_conditie=query_object_evtp_gst.entity_gst.conditie,
            evtp_gebrdl=query_object_evtp_gst.entity_evtp_version.gebr_dl,
            rge=[
                schemas.RgeShort(
                    titel=rge.entity_rge.titel,
                    re_link=rge.entity_rge.re_link,
                )
                for rge in sorted(
                    query_object_evtp_gst.entities_gst_rge,
                    key=lambda item: (item.sort_key or 1000, item.entity_rge.titel),
                )
            ],
        ),
    )


def download_evtp(db: Session) -> StreamingResponse:
    query_object = (
        db.execute(
            select(models.evtp.EvtpVersion)
            .filter(models.evtp.EvtpVersion.id_publicatiestatus.in_(PUBLICATION_RANGE))
            .order_by(models.evtp.EvtpVersion.evtp_nm)
        )
        .scalars()
        .all()
    )

    data = [schemas.evtp.EvtpVersion.model_validate(r).model_dump() for r in query_object]
    df = pd.json_normalize(data)
    columns = [str(c) for c in df.columns]
    relevant_columns = [
        c
        for c in columns
        if c not in ["evtp_cd", "user_nm", "notitie", "lidw_soort_besluit", "soort_besluit", "sort_key", "versie_nr"]
    ]

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

    stream = io.StringIO()
    df.to_csv(stream, index=False, quoting=csv.QUOTE_ALL)

    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers[
        "Content-Disposition"
    ] = f"attachment; filename=besluiten_dump_{datetime.now().strftime('%Y%m%d')}.csv"
    response.headers["Content-Encoding"] = "UTF-8"
    response.headers["Content-type"] = "text/csv; charset=UTF-8"

    return response


def get_by_publicatiestatus_oe(db: Session):
    results = db.execute(
        select(
            models.oe.Oe.naam_officieel,
            func.count(models.evtp.EvtpVersion.id_publicatiestatus),
        )
        .join(models.oe.Oe)
        .where(
            and_(
                models.evtp.EvtpVersion.id_publicatiestatus.in_(PUBLICATION_RANGE),
                models.evtp.EvtpVersion.huidige_versie.in_(CURRENT_VERSION),
            )
        )
        .group_by(models.oe.Oe.naam_officieel)
        .order_by(desc(func.count(models.evtp.EvtpVersion.id_publicatiestatus)))
    ).all()

    oe_by_evtp = [
        OeByEvtp(
            naam_officieel=naam,
            count=count,
        )
        for naam, count in results
    ]
    return OeByEvtpTotal(oe_by_evtp_total=oe_by_evtp)


def get_search_suggestion(db: Session, search_query: str, limit: int = 100):
    model_evtp_version = models.evtp.EvtpVersion
    query_filters = get_base_query_filters()

    if search_query:
        filter_ilike = model_evtp_version.evtp_nm.ilike(f"%{search_query}%")
        filter_synonyms = model_evtp_version.vector_suggestion.op("@@")(func.websearch_to_tsquery("NLD", search_query))
        similarity_score = func.similarity(model_evtp_version.evtp_nm, search_query)

        query = (
            select(model_evtp_version)
            .where(and_(*query_filters, or_(filter_ilike, filter_synonyms)))
            .order_by(desc(similarity_score))
        )

        query_evtp = db.execute(query.limit(limit)).scalars().all()

        if not query_evtp:
            logger.info("Suggestion search - ilike did not give any results for besluiten")
            search_condition = get_similarity_search_clause(
                search_query, model=model_evtp_version, suggestion_search=True
            )
            query_filters.append(search_condition)
            query = (
                select(model_evtp_version, similarity_score)
                .where(and_(*query_filters))
                .order_by(desc(similarity_score))
            )
            query_evtp = db.execute(query.limit(limit)).scalars().all()
            if query_evtp:
                logging.info(f"Suggestion-search - Similarity search query for besluiten for: {search_query}")
            else:
                logging.info("Suggestion-search - Similarity search did not give any results for besluiten")
        else:
            logging.info(f"Suggestion search - Ilike search with synonyms results for besluiten for: {search_query}")
    else:
        query = select(model_evtp_version).where(and_(*query_filters))
        query_evtp = db.execute(query.limit(limit)).scalars().all()

    return schemas.common.SearchSuggestionsAllEntities(
        gg=[],
        evtp=[
            schemas.common.SearchSuggestion(
                title=query_object.evtp_nm, upc=query_object.evtp_upc, version=query_object.versie_nr
            )
            for query_object in query_evtp
        ],
        oe=[],
    )
