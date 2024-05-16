import logging
from typing import Literal

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import app.crud as crud
import app.schemas as schemas
from app.api import dependencies
from app.database.database import get_async_session

# Setup logger
logger = logging.getLogger(__name__)

# Create router for login functionalities
router = APIRouter()


@router.get("/health-db")
async def healthcheck_db(
    db: AsyncSession = Depends(get_async_session),
) -> Literal["OK"]:
    """
    Check whether the database still responds
    """
    await db.execute(select(1))  # random query
    return "OK"


@router.get("/health-backend")
def healthcheck_backend() -> Literal["OK"]:
    """
    Check whether the backend still responds
    """
    return "OK"


@router.get("/login/verifieer", response_model=schemas.gebruiker.Gebruiker)
def verify_login(
    current_gebruiker: schemas.gebruiker.Gebruiker = Depends(dependencies.get_current_gebruiker),
) -> schemas.gebruiker.Gebruiker:
    """
    Verifies whether a user is logged on or not.

    Returns: The logged on user if a user is logged on, HTTP 401 otherwise.
    """
    return current_gebruiker


@router.get("/pod-env")
async def get_all() -> list[dict[str, str]]:
    return await crud.pod_env.get_all()
