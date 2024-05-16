import logging
from datetime import datetime
from typing import Any, Callable, Dict, List, Literal, Sequence

import pandas as pd
from pytz import timezone
from sqlalchemy import Boolean, ScalarResult, String, and_, cast, desc, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload

import app.models as models
import app.schemas as schemas
from app.config.resource import LIMIT_RESULTS_QUERY, MappingPublicatiestatus
from app.crud._default_crud_operations import _get_relationships
from app.util.misc import create_upc

# Setup logger
logger = logging.getLogger(__name__)
BASE_MODEL = models.evtp.EvtpVersion

subquery_evtp = (
    select(
        BASE_MODEL.evtp_cd,
        func.max(BASE_MODEL.versie_nr)
        .filter(BASE_MODEL.id_publicatiestatus != MappingPublicatiestatus.ARCHIVED.value[0])
        .label("latest_version"),
    )
    .group_by(BASE_MODEL.evtp_cd)
    .subquery()
)


async def get_all(db: AsyncSession) -> Sequence[BASE_MODEL]:
    """
    Gets all evtp with the highest versie_nr
    Returns: List of evtp objects
    """
    relationships = _get_relationships(base_model=BASE_MODEL)
    eager_loads = [joinedload(getattr(BASE_MODEL, rel)) for rel in relationships]
    result = await db.execute(
        select(BASE_MODEL)
        .options(*eager_loads)
        .join(
            subquery_evtp,
            and_(
                BASE_MODEL.evtp_cd == subquery_evtp.c.evtp_cd,
                BASE_MODEL.versie_nr == subquery_evtp.c.latest_version,
            ),
        )
        .filter(BASE_MODEL.id_publicatiestatus < MappingPublicatiestatus.ARCHIVED.value[0])
        .order_by(BASE_MODEL.ts_mut.desc())
        .limit(LIMIT_RESULTS_QUERY)
    )
    return result.scalars().unique().all()


async def get_list(db: AsyncSession) -> Sequence[BASE_MODEL]:
    """
    Gets all evtp with the highest versie_nr
    Returns: List of evtp objects
    """
    result = await db.execute(
        select(BASE_MODEL)
        .join(
            subquery_evtp,
            and_(
                BASE_MODEL.evtp_cd == subquery_evtp.c.evtp_cd,
                BASE_MODEL.versie_nr == subquery_evtp.c.latest_version,
            ),
        )
        .filter(BASE_MODEL.id_publicatiestatus < MappingPublicatiestatus.ARCHIVED.value[0])
        .order_by(BASE_MODEL.ts_mut.desc())
    )
    return result.scalars().unique().all()


async def get_filtered(
    search_query: str,
    db: AsyncSession,
) -> Sequence[BASE_MODEL]:
    """
    Retrieve filtered records from the database based on the search query.

    Args:
        search_query: The search query to filter the records.
        limit: The maximum number of records to retrieve. Defaults to 100.

    Returns: A list of filtered records.
    """
    search_query = search_query.lower()
    conditions = []
    search_fields = [c.key for c in BASE_MODEL.__table__.columns]

    # Get all relationships of the base model
    relationships = _get_relationships(base_model=BASE_MODEL)
    eager_loads = [joinedload(getattr(BASE_MODEL, rel)) for rel in relationships]

    # Search in all columns of the base model
    for field in search_fields:
        column = getattr(BASE_MODEL, field)
        if not isinstance(column.type, Boolean):
            # For non-boolean columns, use lower() and contains()
            conditions.append(func.lower(cast(column, String)).contains(search_query))

    # Search in the relationship 'verantwoordelijke_oe' on 'naam_officieel'
    verantwoordelijke_oe_rel = getattr(BASE_MODEL, "verantwoordelijke_oe")
    verantwoordelijke_oe_model = verantwoordelijke_oe_rel.property.mapper.class_
    naam_officieel_column = getattr(verantwoordelijke_oe_model, "naam_officieel")
    conditions.append(func.lower(naam_officieel_column).contains(search_query))

    result = await db.execute(
        select(BASE_MODEL)
        .options(*eager_loads)
        .join(
            subquery_evtp,
            and_(
                BASE_MODEL.evtp_cd == subquery_evtp.c.evtp_cd,
                BASE_MODEL.versie_nr == subquery_evtp.c.latest_version,
            ),
        )
        .join(verantwoordelijke_oe_rel)
        .where(or_(*conditions))
        .filter(BASE_MODEL.id_publicatiestatus < MappingPublicatiestatus.ARCHIVED.value[0])
        .order_by(BASE_MODEL.ts_mut.desc())
        .limit(LIMIT_RESULTS_QUERY)
    )
    query = result.scalars().unique().all()
    return query


async def get_all_including_all_versions(db: AsyncSession) -> ScalarResult[BASE_MODEL]:
    """
    Gets all evtp with all versions
    Returns: List of evtp objects
    """
    return await db.scalars(select(BASE_MODEL).order_by(BASE_MODEL.ts_mut.desc()))


async def get_one(db: AsyncSession, evtp_cd: int) -> BASE_MODEL | None:
    """
    Gets an evtp based on the primary key and latest version number.
    Returns: evtp object
    """
    # Get all relationships of the base model
    relationships = _get_relationships(base_model=BASE_MODEL)
    eager_loads = [joinedload(getattr(BASE_MODEL, rel)) for rel in relationships]

    subquery = (
        select(
            BASE_MODEL.evtp_cd,
            func.max(BASE_MODEL.versie_nr).label("latest_version"),
        )
        .group_by(BASE_MODEL.evtp_cd)
        .subquery()
    )

    return await db.scalar(
        select(BASE_MODEL)
        .options(*eager_loads)
        .join(
            subquery,
            and_(
                BASE_MODEL.evtp_cd == subquery.c.evtp_cd,
                BASE_MODEL.versie_nr == subquery.c.latest_version,
            ),
        )
        .filter(BASE_MODEL.evtp_cd == evtp_cd)
    )


def get_tree_structure_one(
    db: Session,
    evtp_cd: int,
    versie_nr: int,
) -> BASE_MODEL | None:
    """
    Gets the evtp underlying structure.
    Used for visualisation of evtp tree structure.
    Returns: evtp_structure object
    """
    relationships = [rel.key for rel in BASE_MODEL.__mapper__.relationships]
    eager_loads = [joinedload(getattr(BASE_MODEL, rel)) for rel in relationships]

    # relationship entities_gst_gstt required eager loading to properly compare with evtp_version timestapms
    eager_loads.append(
        joinedload(models.evtp.EvtpVersion.entities_evtp_gst)
        .joinedload(models.evtp.EvtpGst.entity_gst)
        .joinedload(models.gst.Gst.entities_gst_gstt)
    )

    result = db.execute(
        select(BASE_MODEL)
        .options(*eager_loads)
        .where(
            and_(
                BASE_MODEL.evtp_cd == evtp_cd,
                BASE_MODEL.versie_nr == versie_nr,
            )
        )
    )
    evtp_version = result.unique().scalar()

    return evtp_version


async def update_one(
    db: AsyncSession,
    body: schemas.evtp_version.EvtpVersionIn,
    evtp_cd: int,
    versie_nr: int | None,
    gebruiker: str | None,
) -> BASE_MODEL | None:
    """
    Update an evtp by primary key.

    Args:
        body: The updated evtp version data.
        evtp_cd: The primary key of the evtp.
        versie_nr: The version number of the evtp.
        gebruiker: The user name.

    Returns: The updated evtp version.
    """
    model = BASE_MODEL
    relationships = _get_relationships(base_model=BASE_MODEL)
    eager_loads = [joinedload(getattr(BASE_MODEL, rel)) for rel in relationships]
    payload = {
        **body.model_dump(exclude_unset=True),
        "ts_mut": datetime.now(tz=timezone("Europe/Amsterdam")),
        "user_nm": gebruiker,
    }

    async with db.begin():
        await db.execute(
            update(model)
            .where(and_(model.evtp_cd == evtp_cd, model.versie_nr == versie_nr))
            .values(payload)
            .execution_options(synchronize_session="fetch")
        )

    return await db.scalar(
        select(model).options(*eager_loads).where(and_(model.evtp_cd == evtp_cd, model.versie_nr == versie_nr))
    )


async def update_id_pub(
    db: AsyncSession,
    body: schemas.evtp_version.EvtpVersionStatus,
    evtp_cd: int,
    versie_nr: int,
    gebruiker: str | None,
) -> Literal["OK"]:
    """
    Update an evtp id_publicatiestatus by primary key and versie number.

    Args:
        body: The body containing the updated evtp version status.
        evtp_cd: The primary key of the evtp.
        versie_nr: The version number of the evtp.
        gebruiker: The user name.

    Returns: The result of the update operation.
    """
    current_date = datetime.now(tz=timezone("Europe/Amsterdam"))
    model = BASE_MODEL
    _result = await db.execute(select(model.ts_publ).filter(model.evtp_cd == evtp_cd, model.versie_nr == versie_nr))
    evtp_ts_publ = _result.scalar_one()
    payload = {
        **body.model_dump(exclude_unset=True),
        "ts_mut": current_date,
        "user_nm": gebruiker,
        "huidige_versie": True if body.id_publicatiestatus == 3 else False,
        "ts_publ": (
            evtp_ts_publ if evtp_ts_publ is not None else current_date if body.id_publicatiestatus == 3 else None
        ),
    }

    # Set huidige_versie to False for all other versions when id_publicatiestatus is 3
    if body.id_publicatiestatus == 3:
        await db.execute(
            update(model)
            .where(
                and_(
                    model.evtp_cd == evtp_cd,
                    model.versie_nr != versie_nr,
                    model.id_publicatiestatus == 3,
                )
            )
            .values(
                {
                    "huidige_versie": False,
                    "id_publicatiestatus": 2,
                }
            )
        )

    # Set id_publicatiestatus to 4 for all versions if evtp is archived
    elif body.id_publicatiestatus == MappingPublicatiestatus.ARCHIVED.value[0]:
        await db.execute(
            update(model)
            .where(
                and_(
                    model.evtp_cd == evtp_cd,
                )
            )
            .values(
                {
                    "huidige_versie": False,
                    "id_publicatiestatus": MappingPublicatiestatus.ARCHIVED.value[0],
                }
            )
        )

    await db.execute(
        update(model)
        .where(and_(model.evtp_cd == evtp_cd, model.versie_nr == versie_nr))
        .values(payload)
        .execution_options(synchronize_session="fetch")
    )
    await db.commit()

    return "OK"


async def create_one(db: AsyncSession, body: schemas.evtp_version.EvtpVersionIn, gebruiker: str | None) -> BASE_MODEL:
    """
    Create a new evtp_version record in the database.

    Args:
        body: The input data for creating the evtp_version.
        gebruiker: The user name.

    Returns: The created evtp_version record.
    """
    model_evtp = models.evtp.Evtp
    model_evtp_version = BASE_MODEL

    async with db.begin():
        result = await db.execute(select(model_evtp.evtp_upc))
        list_evtp_upc = result.scalars().all()

        while True:
            evtp_upc = create_upc()
            if evtp_upc not in list_evtp_upc:
                break

        payload_evtp = {
            "evtp_upc": evtp_upc,
        }

        evtp = model_evtp(**payload_evtp)
        db.add(evtp)
        await db.flush()
        await db.refresh(evtp)

        payload_evtp_version = {
            **body.model_dump(exclude_unset=True),
            "ts_mut": datetime.now(tz=timezone("Europe/Amsterdam")),
            "ts_start": datetime.now(tz=timezone("Europe/Amsterdam")),
            "user_nm": gebruiker,
            "evtp_cd": evtp.evtp_cd,
            "versie_nr": 1,
            "id_publicatiestatus": 1,
            "huidige_versie": False,
        }

        evtp_version = model_evtp_version(**payload_evtp_version)
        db.add(evtp_version)  # Add the evtp_version instance to the session

    await db.refresh(evtp_version)  # Refresh the evtp_version instance
    return evtp_version


async def get_all_versions(db: AsyncSession, evtp_cd: int) -> Sequence[int]:
    """
    Gets all the different versions of an evtp

    Args:
        evtp_cd: The evtp primary key

    Returns: A list of evtp version objects
    """
    result = await db.execute(
        select(BASE_MODEL.versie_nr)
        .where(
            and_(
                BASE_MODEL.id_publicatiestatus < MappingPublicatiestatus.ARCHIVED.value[0],
                BASE_MODEL.evtp_cd == evtp_cd,
            )
        )
        .order_by(BASE_MODEL.versie_nr.desc())
    )
    return result.scalars().all()


async def get_one_version(db: AsyncSession, evtp_cd: int, versie_nr: int) -> BASE_MODEL | None:
    """
    Gets one specific version of an evtp objeect
    Returns: one evtp version
    """
    relationships = _get_relationships(base_model=BASE_MODEL)
    eager_loads = [joinedload(getattr(BASE_MODEL, rel)) for rel in relationships]
    return await db.scalar(
        select(BASE_MODEL)
        .where(
            and_(
                BASE_MODEL.versie_nr == versie_nr,
                BASE_MODEL.evtp_cd == evtp_cd,
            )
        )
        .options(*eager_loads)
    )


async def duplicate(
    db: AsyncSession,
    evtp_cd: int,
    body: schemas.evtp_version.EvtpNewVersionIn,
    gebruiker: str | None,
) -> BASE_MODEL | None:
    """
    Create a duplicate of an evtp but with a new primary key and upc. This created all the related objects as well.

    Args:
        evtp_cd: The evtp code.
        body: The request body containing the new version data.
        gebruiker: The user name. Defaults to None.

    Returns: The newly created version of the evtp.

    """

    model_evtp = models.evtp.Evtp
    model_evtp_version = BASE_MODEL
    relationships = _get_relationships(base_model=BASE_MODEL)
    eager_loads = [joinedload(getattr(BASE_MODEL, rel)) for rel in relationships]
    current_date = datetime.now(tz=timezone("Europe/Amsterdam"))

    async with db.begin():
        result = await db.execute(select(model_evtp.evtp_upc))
        list_evtp_upc = result.scalars().all()

        while True:
            evtp_upc = create_upc()
            if evtp_upc not in list_evtp_upc:
                break

        payload_evtp = {
            "evtp_upc": evtp_upc,
        }

        evtp = model_evtp(**payload_evtp)
        db.add(evtp)
        await db.flush()
        await db.refresh(evtp)

        payload_evtp_version = {
            **body.model_dump(exclude_unset=True),
            "ts_mut": datetime.now(tz=timezone("Europe/Amsterdam")),
            "ts_start": datetime.now(tz=timezone("Europe/Amsterdam")),
            "user_nm": gebruiker,
            "evtp_cd": evtp.evtp_cd,
            "versie_nr": 1,
            "id_publicatiestatus": 1,
            "huidige_versie": False,
        }

        evtp_version = model_evtp_version(**payload_evtp_version)
        db.add(evtp_version)  # Add the evtp_version instance to the session

        # Create related models with new versions
        await create_related_models(
            db=db,
            existing_evtp_cd=evtp_cd,
            current_date=current_date,
            gebruiker=gebruiker or "ICTU",
            new_evtp_cd=evtp.evtp_cd,
        )

    return await db.scalar(
        select(model_evtp_version)
        .options(*eager_loads)
        .filter(model_evtp_version.evtp_cd == evtp_cd, model_evtp_version.versie_nr == body.versie_nr)
    )


async def create_new_version(
    db: AsyncSession,
    evtp_cd: int,
    body: schemas.evtp_version.EvtpNewVersionIn,
    gebruiker: str | None,
) -> BASE_MODEL | None:
    """
    Create a new version of an evtp. This created all the related objects as well.

    Args:
        evtp_cd: The evtp code.
        body: The request body containing the new version data.
        gebruiker: The user name. Defaults to None.

    Returns: The newly created version of the evtp.

    """
    model = BASE_MODEL
    relationships = _get_relationships(base_model=BASE_MODEL)
    eager_loads = [joinedload(getattr(BASE_MODEL, rel)) for rel in relationships]

    async with db.begin():
        # Modify existing evtp but set enddate
        current_date = datetime.now(tz=timezone("Europe/Amsterdam"))
        previous_version = await db.scalar(
            select(model).filter(model.evtp_cd == evtp_cd).order_by(desc(model.versie_nr)).limit(1)
        )
        previous_version.ts_end = current_date  # type: ignore

        # Add new evtp with the same evtp_upc
        payload = {
            **body.model_dump(exclude_unset=True),
            "huidige_versie": False,
            "evtp_cd": evtp_cd,
            "ts_mut": current_date,
            "ts_start": current_date,
            "user_nm": gebruiker or "",  # Provide a default value for gebruiker
            "id_publicatiestatus": 1,
        }
        evtp = model(**payload)
        db.add(evtp)

        # Create related models with new versions
        await create_related_models(
            db=db, existing_evtp_cd=evtp_cd, current_date=current_date, gebruiker=gebruiker or "ICTU"
        )

    return await db.scalar(
        select(model).options(*eager_loads).filter(model.evtp_cd == evtp_cd, model.versie_nr == body.versie_nr)
    )


async def create_related_models(
    db: AsyncSession, existing_evtp_cd: int, current_date: datetime, gebruiker: str, new_evtp_cd: int = 0
) -> None:
    """
    Creates related models for a given evtp_cd.

    Args:
        evtp_cd: The evtp_cd value.
        current_date: The current date.
        gebruiker: The user name.
    """
    # Set enddate for all related evtp_gst and create duplicates with different startdate
    evtp_gst_list = await db.scalars(
        select(models.evtp.EvtpGst).where(
            and_(
                models.evtp.EvtpGst.evtp_cd == existing_evtp_cd,
                models.evtp.EvtpGst.ts_end > current_date,
            )
        )
    )

    new_evtp_onds: List[models.ond.EvtpOnd] = []
    new_evtp_oe_com_types: List[models.evtp.EvtpOeComType] = []
    new_evtp_gsts: List[models.evtp.EvtpGst] = []
    new_gst_gstts: List[models.gst.GstGstt] = []
    new_gst_ggs: List[models.gst.GstGg] = []
    new_gst_rges: List[models.gst.GstRge] = []

    # Create new evtp_ond objects
    evtp_ond_list = await db.scalars(
        select(models.ond.EvtpOnd).filter(
            and_(
                models.ond.EvtpOnd.evtp_cd == existing_evtp_cd,
                models.ond.EvtpOnd.ts_end > current_date,
            )
        )
    )

    for evtp_ond in evtp_ond_list:
        evtp_ond.ts_end = current_date
        new_evtp_ond = models.ond.EvtpOnd(
            evtp_cd=new_evtp_cd if new_evtp_cd else evtp_ond.evtp_cd,
            ond_cd=evtp_ond.ond_cd,
            user_nm=gebruiker,
            ts_mut=current_date,
            ts_start=current_date,
            ts_end=datetime(9999, 12, 31),
        )
        new_evtp_onds.append(new_evtp_ond)

    # Create new evtp_oe_com objects
    evtp_oe_com_list = await db.scalars(
        select(models.evtp.EvtpOeComType).filter(
            and_(
                models.evtp.EvtpOeComType.evtp_cd == existing_evtp_cd,
                models.evtp.EvtpOeComType.ts_end > current_date,
            )
        )
    )

    for evtp_oe_com in evtp_oe_com_list:
        evtp_oe_com.ts_end = current_date
        new_evtp_oe_com_type = models.evtp.EvtpOeComType(
            evtp_cd=new_evtp_cd if new_evtp_cd else evtp_oe_com.evtp_cd,
            oe_com_type_cd=evtp_oe_com.oe_com_type_cd,
            link=evtp_oe_com.link,
            notitie=evtp_oe_com.notitie,
            user_nm=gebruiker,
            ts_mut=current_date,
            ts_start=current_date,
            ts_end=datetime(9999, 12, 31),
        )
        new_evtp_oe_com_types.append(new_evtp_oe_com_type)

    # Create new evtp_gst objects
    for evtp_gst in evtp_gst_list:
        evtp_gst.ts_end = current_date
        new_evtp_gst = models.evtp.EvtpGst(
            evtp_cd=new_evtp_cd if new_evtp_cd else evtp_gst.evtp_cd,
            gst_cd=evtp_gst.gst_cd,
            sort_key=evtp_gst.sort_key,
            notitie=evtp_gst.notitie,
            conditie=evtp_gst.conditie,
            user_nm=gebruiker,
            ts_mut=current_date,
            ts_start=current_date,
            ts_end=datetime(9999, 12, 31),
        )
        new_evtp_gsts.append(new_evtp_gst)

        await create_gst_related_models(
            db, evtp_gst.gst_cd, current_date, gebruiker, new_gst_gstts, new_gst_ggs, new_gst_rges
        )

    db.add_all(new_evtp_onds)
    db.add_all(new_evtp_oe_com_types)
    db.add_all(new_evtp_gsts)
    db.add_all(new_gst_gstts)
    db.add_all(new_gst_ggs)
    db.add_all(new_gst_rges)


async def create_gst_related_models(
    db: AsyncSession,
    gst_cd: int,
    current_date: datetime,
    gebruiker: str,
    new_gst_gstts: List[models.gst.GstGstt],
    new_gst_ggs: List[models.gst.GstGg],
    new_gst_rges: List[models.gst.GstRge],
) -> None:
    """
    Creates duplicate models with different start dates and sets end dates for related models.

    Args:
        gst_cd: The gst primary key.
        current_date: The current date.
        gebruiker The user name.
        new_gst_gstts: The list of new GstGstt models.
        new_gst_ggs: The list of new GstGg models.
        new_gst_rges: The list of new GstRge models.

    """
    # Set enddate for all related gst_gstt and create duplicates with different startdate
    gst_gstt_list = await db.scalars(
        select(models.gst.GstGstt).filter(
            and_(
                models.gst.GstGstt.gst_cd == gst_cd,
                models.gst.GstGstt.ts_end > current_date,
            )
        )
    )

    for gst_gstt in gst_gstt_list:
        gst_gstt.ts_end = current_date
        new_gst_gstt = models.gst.GstGstt(
            gst_cd=gst_gstt.gst_cd,
            gstt_cd=gst_gstt.gstt_cd,
            notitie=gst_gstt.notitie,
            ts_start=current_date,
            ts_end=datetime(9999, 12, 31),
            user_nm=gebruiker,
            ts_mut=current_date,
        )
        new_gst_gstts.append(new_gst_gstt)

    # Set enddate for all related gst_gg and create duplicates with different startdate
    gst_gg_list = await db.scalars(
        select(models.gst.GstGg).filter(
            and_(
                models.gst.GstGg.gst_cd == gst_cd,
                models.gst.GstGg.ts_end > current_date,
            )
        )
    )
    for gst_gg in gst_gg_list:
        gst_gg.ts_end = current_date
        new_gst_gg = models.gst.GstGg(
            gst_cd=gst_gg.gst_cd,
            gg_cd=gst_gg.gg_cd,
            sort_key=gst_gg.sort_key,
            notitie=gst_gg.notitie,
            user_nm=gebruiker,
            ts_mut=current_date,
            ts_start=current_date,
            ts_end=datetime(9999, 12, 31),
        )
        new_gst_ggs.append(new_gst_gg)

    # Set enddate for all related gst_rge and create duplicates with different startdate
    gst_rge_list = await db.scalars(
        select(models.gst.GstRge).filter(
            and_(
                models.gst.GstRge.gst_cd == gst_cd,
                models.gst.GstRge.ts_end > current_date,
            )
        )
    )
    for gst_rge in gst_rge_list:
        gst_rge.ts_end = current_date
        new_gst_rge = models.gst.GstRge(
            gst_cd=gst_rge.gst_cd,
            rge_cd=gst_rge.rge_cd,
            sort_key=gst_rge.sort_key,
            notitie=gst_rge.notitie,
            user_nm=gebruiker,
            ts_mut=current_date,
            ts_start=current_date,
            ts_end=datetime(9999, 12, 31),
        )
        new_gst_rges.append(new_gst_rge)


async def get_by_publicatiestatus_evtp(db: AsyncSession) -> Dict[str, Callable[[Any], int]]:
    """
    Gets the besluit by publicatiestatus.

    Returns:
    A dictionary containing the count of besluit for each publicatiestatus.
    The keys of the dictionary are the publicatiestatus values, and the values are the counts.
    If a publicatiestatus is not found, it is labeled as "Onbekend" .
    """
    result = await db.execute(
        select(
            BASE_MODEL.id_publicatiestatus,
            func.count(BASE_MODEL.id_publicatiestatus),
        ).group_by(BASE_MODEL.id_publicatiestatus)
    )
    status_count = result.all()

    sorted_status_count = sorted(
        status_count,
        key=lambda row: [member.value[1] for member in MappingPublicatiestatus].index(
            next(
                (member.value[1] for member in MappingPublicatiestatus if member.value[0] == row.id_publicatiestatus),
                "Onbekend",
            )
        ),
    )

    return {
        next(
            (member.value[1] for member in MappingPublicatiestatus if member.value[0] == row.id_publicatiestatus),
            "Onbekend",
        ): row.count
        for row in sorted_status_count
    }


async def get_by_publicatiestatus_oe(db: AsyncSession, top: int = 20):
    """
    Gets the responsible organisation for each besluit by publicatiestatus.

    Args:
        top: The number of top results to return (default is 20).

    Returns:
        A dictionary containing the pivot table data with the responsible organisation for each besluit by publicatiestatus.
        The dictionary is in the following format:
        {
            "index": [list of unique values from the 'naam_officieel' column],
            "columns": [list of unique values from the 'id_publicatiestatus' column],
            "data": [2D list representing the pivot table data],
            "aggfunc": "sum",
            "fill_value": 0,
            "margins": True,
            "margins_name": "Totaal"
        }
    """
    result = await db.execute(
        select(
            BASE_MODEL.id_publicatiestatus,
            models.oe.Oe.naam_officieel,
            func.count(BASE_MODEL.id_publicatiestatus),
        )
        .join(models.oe.Oe)
        .group_by(BASE_MODEL.id_publicatiestatus, models.oe.Oe.naam_officieel)
    )

    data = result.all()

    df = pd.DataFrame(data, columns=["id_publicatiestatus", "naam_officieel", "count"])
    df["id_publicatiestatus"] = df["id_publicatiestatus"].map(
        lambda x: next((member.value[1] for member in MappingPublicatiestatus if member.value[0] == x), "Onbekend")
    )

    desired_order = [member.value[1] for member in MappingPublicatiestatus]
    present_statuses = [status for status in desired_order if status in df["id_publicatiestatus"].unique()] + ["Totaal"]
    pivot_table = df.pivot_table(
        index="naam_officieel",
        columns="id_publicatiestatus",
        values="count",
        aggfunc="sum",
        fill_value=0,
        margins=True,
        margins_name="Totaal",
    )

    sorted_pivot = pivot_table[present_statuses].sort_values(by="Totaal", ascending=False)
    return sorted_pivot.iloc[1:top].to_dict(orient="split")
