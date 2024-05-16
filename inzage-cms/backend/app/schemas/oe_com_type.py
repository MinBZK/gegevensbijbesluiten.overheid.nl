from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class OeComType(BaseModel):
    oe_com_type_cd: int
    omschrijving: str
    notitie: str | None
    user_nm: str
    ts_mut: datetime


class OeComTypeMinimalList(BaseModel):
    oe_com_type_cd: int
    omschrijving: str


class OeComTypeIn(BaseModel):
    omschrijving: str
    notitie: str | None = None
