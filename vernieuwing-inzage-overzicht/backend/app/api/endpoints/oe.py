import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.schemas as schemas
from app import crud
from app.database.database import (
    get_sync_session,
)

# Setup logger
logger = logging.getLogger(__name__)

# Create router for login functionalities
router = APIRouter()


@router.get("/{oe_upc}")
async def get_one(
    oe_upc: int,
    db: Session = Depends(get_sync_session),
):
    return crud.oe.get_details(db, oe_upc)


@router.post("/filter")
async def get_filtered(
    search_query: schemas.oe.OeQuery,
    db: Session = Depends(get_sync_session),
):
    return crud.oe.get_filtered(db, search_query)
