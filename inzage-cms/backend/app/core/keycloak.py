import logging
import os
import time

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from jwt.exceptions import ExpiredSignatureError
from keycloak import KeycloakOpenID

logger = logging.getLogger(__name__)

URI = os.getenv("KEYCLOAK_URI", "https://test.nl")
CLIENT = os.getenv("KEYCLOAK_CLIENT", "test")
REALM = os.getenv("KEYCLOAK_REALM", "test")

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{URI}/realms/{REALM}/protocol/openid-connect/auth",
    tokenUrl=f"{URI}/realms/{REALM}/protocol/openid-connect/token",
)

cache = dict()


class UserUnauthorizedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inloggegevens konden niet succesvol worden gevalideerd.",
            headers={"WWW-Authenticate": "Bearer"},
        )


def _update_public_key(keycloak_openid: KeycloakOpenID, update_interval=30):
    """
    Update cache by fetching a new public key
    Returns false if last update is less than <update_interval> seconds ago to prevent overusage and infinite loops
    """
    if time.time() - cache["keycloak_public_key_updated"] > update_interval:
        cache["keycloak_public_key"] = keycloak_openid.public_key()
        cache["keycloak_public_key_updated"] = time.time()
        return True
    return False


def _get_public_key(keycloak_openid: KeycloakOpenID):
    if "keycloak_public_key" not in cache:
        logger.info("fetching public key")
        cache["keycloak_public_key"] = keycloak_openid.public_key()
        cache["keycloak_public_key_updated"] = time.time()
    return cache["keycloak_public_key"]


def _decode_token(token: str):
    """
    Fetch the public key from Keycloak and decode the token from the frontend.
    Note: Data in the token is NOT encrypted. the public key is only to validate.
    """
    logger.info("authorizing")
    # public access type
    keycloak_openid = KeycloakOpenID(
        server_url=URI,
        client_id=CLIENT,
        realm_name=REALM,
    )

    public_key = _get_public_key(keycloak_openid)
    KEYCLOAK_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\n" + public_key + "\n-----END PUBLIC KEY-----"
    try:
        decoded = jwt.decode(
            token,
            key=KEYCLOAK_PUBLIC_KEY,
            options={
                "verify_signature": True,
                "verify_aud": False,
                "exp": True,
            },
            algorithms=["RS256"],
        )
        return decoded

    except ExpiredSignatureError:
        logger.info("session expired")
        raise UserUnauthorizedException()

    except jwt.exceptions.DecodeError:
        if _update_public_key(keycloak_openid):
            logger.info("Could not decode token. Updating public key and retry once")
            return _decode_token(token)
        logger.info("Could not decode token")
        raise UserUnauthorizedException()

    except jwt.exceptions.ImmatureSignatureError:
        logger.info("token not yet valid, retrying")
        time.sleep(0.5)
        return _decode_token(token)


def get_current_user(token=Depends(oauth2_scheme)):
    user = _decode_token(token)
    logger.debug(f"received token for {user.get('prefered_username')}")
    return user
