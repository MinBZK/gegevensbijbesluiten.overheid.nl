import json
import logging
from typing import Literal

from fastapi import (
    APIRouter,
)
from fastapi.security import (
    HTTPBasic,
)
from pydantic import BaseModel, Field
from pydantic_settings import (
    BaseSettings,
)

include_in_schema = False
PWD_LENGTH = 64

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBasic()


class Preditor(BaseSettings):
    get_url: str = Field(
        "/api/static-content",
        alias="GET_URL",
    )

    # Fallback contents file
    static_content_path_default: str = Field(
        "app/data/static_content_default.json",
        alias="STATIC_CONTENT_PATH_DEFAULT",
    )


preditor_settings = Preditor()


class StaticContentJson(BaseModel):
    """
    Content in dictionary format: lang { group { field { key, label } } }
    """

    en: dict[str, dict[str, str]]
    nl: dict[str, dict[str, str]]
    fy: dict[str, dict[str, str]]
    pap: dict[str, dict[str, str]]


class UpdateContentRequest(BaseModel):
    publication_status: Literal["published", "draft"]
    static_content_json: StaticContentJson


@router.get(
    preditor_settings.get_url,
    response_model=StaticContentJson,
)
async def get_all_content():
    """Fetch all content."""
    path = preditor_settings.static_content_path_default

    with open(path) as file:
        content: dict[
            str,
            dict[str, dict[str, str]],
        ] = json.load(file)

    return content
