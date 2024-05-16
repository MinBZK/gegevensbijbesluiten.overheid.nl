import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.crud as crud
import app.schemas as schemas
from app.database.database import (
    get_sync_session,
)

# Setup logger
logger = logging.getLogger(__name__)

# Create router for login functionalities
router = APIRouter()


@router.get(
    "/{evtp_upc}/{versie_nr}/gg/",
    response_model=schemas.evtp.EvtpGg,
)
async def get_evtp_gg_version(
    evtp_upc: int,
    versie_nr: int,
    db: Session = Depends(get_sync_session),
):
    return crud.evtp.get_evtp_gg(
        db=db,
        evtp_upc=evtp_upc,
        version_nr=versie_nr,
    )


@router.get(
    "/{evtp_upc}/gg/",
    response_model=schemas.evtp.EvtpGg,
)
async def get_evtp_gg(
    evtp_upc: int,
    db: Session = Depends(get_sync_session),
):
    return crud.evtp.get_evtp_gg(db=db, evtp_upc=evtp_upc)


@router.get(
    "/{evtp_upc}/{versie_nr}/gst/{gst_upc}",
    response_model=schemas.evtp_gg_gst.EvtpGgGst,
)
async def get_evtp_gst_version(
    evtp_upc: int,
    versie_nr: int,
    gst_upc: int,
    db: Session = Depends(get_sync_session),
):
    return crud.evtp.get_evtp_gst(
        db=db,
        evtp_upc=evtp_upc,
        version_nr=versie_nr,
        gst_upc=gst_upc,
    )


@router.get(
    "/{evtp_upc}/gst/{gst_upc}",
    response_model=schemas.evtp_gg_gst.EvtpGgGst,
)
async def get_evtp_gst(
    evtp_upc: int,
    gst_upc: int,
    db: Session = Depends(get_sync_session),
):
    return crud.evtp.get_evtp_gst(
        db=db,
        evtp_upc=evtp_upc,
        gst_upc=gst_upc,
    )
