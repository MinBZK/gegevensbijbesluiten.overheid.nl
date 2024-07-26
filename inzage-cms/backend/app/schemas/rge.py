from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class Rge(BaseModel):
    rge_cd: int
    notitie: str | None
    re_link: str | None
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
