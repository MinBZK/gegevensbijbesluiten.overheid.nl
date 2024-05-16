import logging

from fastapi import Depends

import app.schemas as schemas
from app.core import keycloak

logger = logging.getLogger(__name__)


def get_current_gebruiker(
    user=Depends(keycloak.get_current_user),
) -> schemas.gebruiker.Gebruiker:
    """
    Gets the current logged on user based on the content of the JWT.
    Returns: Model of the currently logged on user.
    """
    if not user.get("preferred_username"):
        logger.error(f"Email has not been configured for {user}")

    gebruiker = schemas.gebruiker.Gebruiker(
        email=user.get("email"),
        name=user.get("preferred_username"),
    )
    return gebruiker
