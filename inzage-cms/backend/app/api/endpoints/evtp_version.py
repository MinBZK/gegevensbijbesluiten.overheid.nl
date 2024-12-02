import logging
from typing import Literal, Sequence

from fastapi import APIRouter, Depends
from sqlalchemy import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

import app.crud as crud
import app.schemas as schemas
from app.database.database import get_async_session, get_sync_session
from app.models.evtp import EvtpVersion
from app.rules.applyRules import ExpertService
from app.schemas.rules import ValidateStructureResult

# Setup logger
logger = logging.getLogger(__name__)

# Create router for login functionalities
router = APIRouter()


@router.get("/", response_model=list[schemas.evtp_version.EvtpVersionWithRelations])
async def get_all(
    *,
    db: AsyncSession = Depends(get_async_session),
) -> Sequence[EvtpVersion]:
    """
    Retrieve all EvtpVersion objects.

    Returns: A list of EvtpVersion with their relations.
    """
    return await crud.evtp_version.get_all(db=db)


@router.get(
    "-list/",
    response_model=list[schemas.evtp_version.EvtpVersionMinimalList],
)
async def get_list(
    *,
    db: AsyncSession = Depends(get_async_session),
) -> Sequence[EvtpVersion]:
    """
    Retrieve a list of EvtpVersion objects.

    Returns: A sequence of EvtpVersion.
    """
    return await crud.evtp_version.get_list(db=db)


@router.get("/{evtp_cd}", response_model=schemas.evtp_version.EvtpVersionWithRelations)
async def get_one(
    evtp_cd: int,
    db: AsyncSession = Depends(get_async_session),
) -> EvtpVersion | None:
    """
    Retrieve a single EvtpVersion object with the specified evtp_cd.

    Args:
        evtp_cd: The primary key of EvtpVersion.

    Returns: The retrieved EvtpVersion if found, otherwise None.
    """
    return await crud.evtp_version.get_one(db=db, evtp_cd=evtp_cd)


@router.put("/{evtp_cd}", response_model=schemas.evtp_version.EvtpVersionWithRelations)
async def update_one(
    body: schemas.evtp_version.EvtpVersionIn,
    evtp_cd: int,
    db: AsyncSession = Depends(get_async_session),
) -> EvtpVersion | None:
    """
    Update an EvtpVersion object with the given ID.

    Args:
        body: The updated EvtpVersion version data.
        evtp_cd: The primary key of EvtpVersion.
        current_gebruiker: The current user.

    Return: The updated EvtpVersion version with its relations.
    """
    return await crud.evtp_version.update_one(
        db=db,
        body=body,
        evtp_cd=evtp_cd,
        versie_nr=body.versie_nr,
        gebruiker="current_gebruiker.name",
    )


@router.get(
    "/partial/{evtp_cd}/{versie_nr}",
    response_model=schemas.evtp_version.EvtpVersionStatus,
)
async def one_partial(
    evtp_cd: int,
    versie_nr: int,
    db: AsyncSession = Depends(get_async_session),
) -> EvtpVersion | None:
    """
    Retrieve a partial EvtpVersion version by its code and version number.

    Args:
        evtp_cd: The primary key of EvtpVersion.
        versie_nr: The version number of the EvtpVersion version.

    Return: The retrieved EvtpVersion version or None if not found.
    """
    return await crud.evtp_version.get_one_version(db=db, evtp_cd=evtp_cd, versie_nr=versie_nr)


@router.get(
    "/filter/{search_query}",
    response_model=list[schemas.evtp_version.EvtpVersionWithRelations],
)
async def get_filtered(
    *,
    search_query: str = "",
    db: AsyncSession = Depends(get_async_session),
) -> Sequence[EvtpVersion]:
    """
    Retrieve a list of filtered EvtpVersions based on the search query.

    Args:
        search_query: The search query to filter the EvtpVersions.

    Return: A list of filtered EvtpVersions.
    """
    return await crud.evtp_version.get_filtered(db=db, search_query=search_query)


@router.post("/", response_model=schemas.evtp_version.EvtpVersion)
async def create_one(
    body: schemas.evtp_version.EvtpVersionIn,
    db: AsyncSession = Depends(get_async_session),
) -> EvtpVersion:
    """
    Create a new EvtpVersion.

    Args:
        body: The data for the new EvtpVersion.
        current_gebruiker: The current user.

    Return: The created EvtpVersion.
    """
    return await crud.evtp_version.create_one(db=db, body=body, gebruiker="current_gebruiker.name")


@router.post("-duplicate/{evtp_cd}", response_model=schemas.evtp_version.EvtpVersion)
async def duplicate(
    evtp_cd: int,
    body: schemas.evtp_version.EvtpNewVersionIn,
    db: AsyncSession = Depends(get_async_session),
) -> EvtpVersion | None:
    """
    Duplicate an evtp version.

    Args:
        evtp_cd: The primary key of EvtpVersion.
        body: The data for the new version.
        current_gebruiker: The current user.

    Returns: The duplicated EvtpVersion, or None if duplication fails.
    """
    return await crud.evtp_version.duplicate(db=db, evtp_cd=evtp_cd, body=body, gebruiker="current_gebruiker.name")


## ---- related to evtp versions ---- ##
@router.get(
    "-list-versions/",
    response_model=list[schemas.evtp_version.EvtpMinimalListIncludingVersions],
)
async def get_all_including_all_versions(
    *,
    db: AsyncSession = Depends(get_async_session),
) -> ScalarResult[EvtpVersion]:
    """
    Retrieve all versions of the EvtpVersion object, including minimal information for each version.

    Returns: A list of EvtpVersion, each containing minimal information.

    """
    return await crud.evtp_version.get_all_including_all_versions(db=db)


@router.get("-versions/{evtp_cd}")
async def get_all_versions(
    evtp_cd: int,
    db: AsyncSession = Depends(get_async_session),
) -> Sequence[int]:
    """
    Retrieve all EvtpVersion boejcts for a given evtp_cd.

    Args:
        evtp_cd: The primary key of EvtpVersion.

    Return: A sequence of all EvtpVersions for the given evtp_cd.
    """
    return await crud.evtp_version.get_all_versions(db=db, evtp_cd=evtp_cd)


@router.get("/{evtp_cd}/{versie_nr}", response_model=schemas.evtp_version.EvtpVersionWithRelations)
async def get_one_version(
    evtp_cd: int,
    versie_nr: int,
    db: AsyncSession = Depends(get_async_session),
) -> EvtpVersion | None:
    """
    Retrieve a specific version of an evtp_cd.

    Args:
        evtp_cd: The primary key of EvtpVersion.
        versie_nr: The versie_nr of the version to retrieve.

    Return: The retrieved version if found, None otherwise.
    """
    return await crud.evtp_version.get_one_version(db=db, evtp_cd=evtp_cd, versie_nr=versie_nr)


@router.post("-version/{evtp_cd}", response_model=schemas.evtp_version.EvtpVersion)
async def create_new_version(
    evtp_cd: int,
    body: schemas.evtp_version.EvtpNewVersionIn,
    db: AsyncSession = Depends(get_async_session),
) -> EvtpVersion | None:
    """
    Create a new EvtpVersion object for the given evtp_cd.

    Args:
        evtp_cd: The primary key of EvtpVersion.
        body: The request body containing the new version data.
        current_gebruiker: The current user.

    Return: The created EvtpVersion or None if creation failed.
    """
    return await crud.evtp_version.create_new_version(
        db=db, evtp_cd=evtp_cd, body=body, gebruiker="current_gebruiker.name"
    )


## ---- related to evtp tree structure ---- ##
@router.get(
    "/relations/{evtp_cd}/{versie_nr}",
    response_model=schemas.evtp_tree_structure.EvtpTreeStructure,
)
async def get_tree_structure_one(
    evtp_cd: int,
    versie_nr: int,
    db: Session = Depends(get_sync_session),
) -> EvtpVersion | None:
    """
    Retrieve the tree structure for a specific EvtpVersion.

    Args:
        evtp_cd: The primary key of EvtpVersion.
        versie_nr: The version number.

    Return: The tree structure of the EvtpVersion, or None if not found.
    """
    return crud.evtp_version.get_tree_structure_one(db=db, evtp_cd=evtp_cd, versie_nr=versie_nr)


@router.get(
    "/relations-validate/{evtp_cd}/{versie_nr}",
)
async def validate_tree_structure_one(
    evtp_cd: int,
    versie_nr: int,
    db: Session = Depends(get_sync_session),
) -> list[ValidateStructureResult]:
    """
    Validates the tree structure for a specific EvtpVerson based on evtp_cd and versie_nr.

    Args:
        evtp_cd: The primary key of EvtpVersion.
        versie_nr: The versie_nr value.

    Return: A list of validation findings.
    """
    schema_dict = schemas.evtp_tree_structure.EvtpTreeStructure.model_validate(
        crud.evtp_version.get_tree_structure_one(db=db, evtp_cd=evtp_cd, versie_nr=versie_nr)
    ).model_dump()
    findings = ExpertService().validate_structure(schema_dict)

    return findings


## ---- related to publicatiestatus ---- ##
@router.put(
    "/change_id_pub/{evtp_cd}/{versie_nr}",
)
async def change_id_pub(
    body: schemas.evtp_version.EvtpVersionStatus,
    evtp_cd: int,
    versie_nr: int,
    db: AsyncSession = Depends(get_async_session),
) -> Literal["OK"]:
    """
    Update the ID publication status for a specific EvtpVersion version.

    Args:
        body: The updated EvtpVersion status.
        evtp_cd: The primary key of EvtpVersion.
        versie_nr: The version number.
        current_gebruiker: The current user.

    Return: The string "OK" indicating a successful update.

    """
    return await crud.evtp_version.update_id_pub(
        db=db,
        body=body,
        evtp_cd=evtp_cd,
        versie_nr=versie_nr,
        gebruiker="current_gebruiker.name",
    )


@router.get(
    "/publicatiestatus/evtp/",
)
async def get_evtp_by_publicatiestatus(
    db: AsyncSession = Depends(get_async_session),
):
    """
    Returns EvtpVersion object by publicatiestatus

    Returns: The EvtpVersion that matches the specified publicatiestatus.
    """
    return await crud.evtp_version.get_by_publicatiestatus_evtp(db=db)


@router.get(
    "/publicatiestatus/oe/",
    response_model=schemas.evtp_version.EvtpOeAggregatedStatus,
)
async def get_evtp_by_publicatiestatus_organisation(
    db: AsyncSession = Depends(get_async_session),
):
    """
    Returns EvtpVersion by publicatiestatus and responsible organisation.

    Returns: The aggregated status of EvtpVersions by responsible organisation.
    """
    return await crud.evtp_version.get_by_publicatiestatus_oe(db=db)
