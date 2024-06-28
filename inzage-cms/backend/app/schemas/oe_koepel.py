from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


# oe
class OeKoepel(BaseModel):
    oe_koepel_cd: int
    titel: str
    omschrijving: str | None
    notitie: str | None
    user_nm: str
    ts_mut: datetime


class OeMinimalList(BaseModel):
    oe_cd: int
    naam_officieel: str


class _OeKoepelOeWithRelations(BaseModel):
    parent_entity: OeKoepelMinimalList
    child_entity: OeMinimalList


class OeKoepelWithRelations(OeKoepel):
    count_children: int
    child_entities: list[_OeKoepelOeWithRelations | None]


class OeKoepelMinimalList(BaseModel):
    oe_koepel_cd: int
    titel: str

    model_config = ConfigDict(from_attributes=True)


class OeKoepelIn(BaseModel):
    titel: str
    omschrijving: str
    notitie: str | None = None
