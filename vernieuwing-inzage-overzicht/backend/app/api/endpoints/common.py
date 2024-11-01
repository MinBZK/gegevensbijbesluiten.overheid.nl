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


@router.get(
    "/suggestion",
    response_model=schemas.common.SearchSuggestionsAllEntities,
)
async def get_search_suggestion(
    search_query: str = Query(default=""),
    db: Session = Depends(get_sync_session),
):
    evtp_suggestions = crud.evtp.get_search_suggestion(db=db, search_query=search_query)
    gg_suggestions = crud.gg.get_search_suggestion(db=db, search_query=search_query)
    oe_suggestions = crud.oe.get_search_suggestion(db=db, search_query=search_query)

    # Combine results
    return schemas.common.SearchSuggestionsAllEntities(
        gg=gg_suggestions.gg, evtp=evtp_suggestions.evtp, oe=oe_suggestions.oe
    )
