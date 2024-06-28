from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.oe import OeMinimalList
from app.schemas.oe_koepel import OeKoepelMinimalList


class OeKoepelOe(BaseModel):
    oe_koepel_oe_cd: int
    oe_koepel_cd: int
    oe_cd: int
    notitie: str | None
    ts_mut: datetime
    user_nm: str


class OeKoepelOeMinimalList(BaseModel):
    oe_koepel_oe_cd: int
    omschrijving: str


class OeKoepelOeWithRelations(OeKoepelOe):
    parent_entity: OeKoepelMinimalList
    child_entity: OeMinimalList

    model_config = ConfigDict(from_attributes=True)


class OeKoepelOeIn(BaseModel):
    notitie: str | None = None
    oe_cd: int
    oe_koepel_cd: int
