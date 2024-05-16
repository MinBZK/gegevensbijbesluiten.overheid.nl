from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.schemas.oe import OeMinimalList


class Ibron(BaseModel):
    ibron_cd: int
    omschrijving: str
    oe_cd: int | None
    user_nm: str
    notitie: str | None
    ts_mut: datetime


class IbronMinimalList(BaseModel):
    ibron_cd: int
    omschrijving: str


class IbronIn(BaseModel):
    omschrijving: str
    oe_cd: int
    notitie: str | None = None


class IbronWithRelations(BaseModel):
    ibron_cd: int
    omschrijving: str
    oe_cd: int | None
    user_nm: str
    notitie: str | None
    ts_mut: datetime

    entity_oe: OeMinimalList | None
