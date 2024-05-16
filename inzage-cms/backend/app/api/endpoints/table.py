import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.crud as crud
import app.schemas as schemas
from app.config.resource import TableResource
from app.database.database import get_sync_session

# Setup logger
logger = logging.getLogger(__name__)

# Create router for login functionalities
router = APIRouter()


@router.get("/{resource}/model", response_model=schemas.table.TableModel)
async def get_model(
    resource: TableResource,
    db: Session = Depends(get_sync_session),
):
    """
    Retrieve the model for a tabel.
    """
    return crud.table.get_model(resource=resource, db=db)
