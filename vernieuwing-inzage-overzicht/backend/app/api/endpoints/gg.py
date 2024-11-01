import logging

from fastapi import APIRouter, Depends, Query
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


@router.post("/filter", response_model=schemas.gg.GgQueryResult)
async def get_filtered(
    search_query: schemas.gg.GgQuery,
    db: Session = Depends(get_sync_session),
) -> schemas.gg.GgQueryResult:
    return crud.gg.get_filtered(db=db, gg_query=search_query)


@router.get(
    "/suggestion",
    response_model=schemas.common.SearchSuggestionsAllEntities,
)
async def get_search_suggestion(
    search_query: str = Query(default=""),
    db: Session = Depends(get_sync_session),
):
    return crud.gg.get_search_suggestion(db=db, search_query=search_query)


@router.get("/{gg_upc}", response_model=schemas.details.GgDetails)
async def get_one(
    gg_upc: int,
    db: Session = Depends(get_sync_session),
) -> schemas.details.GgDetails:
    return crud.gg.get_details(db=db, gg_upc=gg_upc)
