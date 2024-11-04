from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, HttpUrl, field_validator

from app.schemas.oe import OeMinimalList
from app.util.misc import validate_url


class Ibron(BaseModel):
    ibron_cd: int
    titel: str
    afko: str | None
    lidw: str | None
    link: HttpUrl | None
    oe_cd: int | None
    notitie: str | None
    user_nm: str
    ts_mut: datetime


class IbronMinimalList(BaseModel):
    ibron_cd: int
    titel: str


class IbronIn(BaseModel):
    titel: str
    afko: str | None = None
    lidw: str | None = None
    link: str | None = None
    oe_cd: int
    notitie: str | None = None

    _validate_re_link = field_validator("link")(validate_url)


class IbronWithRelations(BaseModel):
    ibron_cd: int
    titel: str | None
    afko: str | None = None
    lidw: str | None
    link: HttpUrl | None
    oe_cd: int | None
    notitie: str | None
    user_nm: str
    ts_mut: datetime

    entity_oe: OeMinimalList | None
