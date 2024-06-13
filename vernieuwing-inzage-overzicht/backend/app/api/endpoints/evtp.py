import logging

from fastapi import APIRouter, Depends
from fastapi.responses import (
    StreamingResponse,
)
from sqlalchemy.orm import Session

import app.crud as crud
import app.schemas as schemas
from app.database.database import (
    get_sync_session,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/filter",
    response_model=schemas.evtp.EvtpQueryResult,
)
async def get_filtered(
    search_query: schemas.evtp.EvtpQuery,
    db: Session = Depends(get_sync_session),
) -> schemas.evtp.EvtpQueryResult:
    return crud.evtp.get_filtered(db=db, evtp_query=search_query)


@router.get("/count")
async def get_count(
    db: Session = Depends(get_sync_session),
) -> int | None:
    return crud.evtp.get_count(db=db)


@router.get("/file")
def download_evtp(
    db: Session = Depends(get_sync_session),
) -> StreamingResponse:
    return crud.evtp.download_evtp(db=db)


@router.get(
    "/statistics-per-oe",
    response_model=schemas.oe.OeByEvtpTotal,
)
async def get_evtp_by_publicatiestatus_organisation(
    db: Session = Depends(get_sync_session),
):
    """
    Returns oe with published evtps
    """
    return crud.evtp.get_by_publicatiestatus_oe(db=db)
