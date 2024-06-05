from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OeComType(BaseModel):
    oe_com_type_cd: int
    omschrijving: str
    notitie: str | None
    user_nm: str
    ts_mut: datetime


class OeComTypeMinimalList(BaseModel):
    oe_com_type_cd: int
    omschrijving: str
    model_config = ConfigDict(from_attributes=True)


class OeComTypeIn(BaseModel):
    omschrijving: str
    notitie: str | None = None
