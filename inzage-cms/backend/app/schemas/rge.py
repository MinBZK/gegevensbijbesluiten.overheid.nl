from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, HttpUrl, field_validator

from app.util.misc import validate_url


class Rge(BaseModel):
    rge_cd: int
    notitie: str | None
    re_link: HttpUrl | None
    tekst: str | None
    titel: str
    ts_mut: datetime
    user_nm: str


class RgeMinimalList(BaseModel):
    rge_cd: int
    titel: str


class RgeIn(BaseModel):
    notitie: str | None = None
    re_link: str
    tekst: str | None = None
    titel: str

    _validate_re_link = field_validator("re_link")(validate_url)
