import logging

from fastapi import (
    APIRouter,
    Depends,
    Query,
)
from sqlalchemy.orm import Session

import app.crud as crud
from app import models, schemas
from app.database.database import (
    get_sync_session,
)

# Setup logger
logger = logging.getLogger(__name__)

# Create router for login functionalities
router = APIRouter()


@router.get(
    "/populated",
    response_model=list[schemas.ond.Ond],
)
async def get_populated(
    db: Session = Depends(get_sync_session),
    limit: int = Query(default=3, ge=1),
) -> list[models.ond.Ond]:
    return crud.ond.get_populated(db=db, limit=limit)


@router.get(
    "/{ond_cd}",
    response_model=list[schemas.evtp.EvtpVersionForOnd],
)
async def get_one(
    ond_cd: int,
    db: Session = Depends(get_sync_session),
):
    return crud.ond.get_one_with_evtps(db=db, ond_cd=ond_cd)
