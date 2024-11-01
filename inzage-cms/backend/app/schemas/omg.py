from __future__ import annotations

from pydantic import BaseModel, ConfigDict, HttpUrl, field_validator

from app.schemas.oe import OeMinimalList
from app.util.misc import validate_url


class Omg(BaseModel):
    omg_cd: int
    titel: str
    oe_cd: int
    lidw: str | None
    link: HttpUrl


class OmgMinimalList(BaseModel):
    omg_cd: int
    titel: str
    model_config = ConfigDict(from_attributes=True)


class OmgIn(BaseModel):
    titel: str
    oe_cd: int
    lidw: str | None = None
    link: str
    notitie: str | None = None

    _validate_re_link = field_validator("link")(validate_url)


class OmgWithRelations(Omg):
    entity_oe: OeMinimalList
