from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.schemas.gg_struct import GgStructWithRelations


class Gg(BaseModel):
    gg_cd: int
    gg_upc: int
    notitie: str | None
    omschrijving: str
    omschrijving_uitgebreid: str | None
    koepel: bool
    ts_mut: datetime
    user_nm: str
    sort_key: int | None


class GgMinimalList(BaseModel):
    gg_cd: int
    omschrijving: str


class GgWithRelations(Gg):
    count_parents: int
    count_children: int
    parent_entities: list[GgStructWithRelations | None]
    child_entities: list[GgStructWithRelations | None]


class GgIn(BaseModel):
    omschrijving: str
    omschrijving_uitgebreid: str
    sort_key: int | None = None
    koepel: bool
    notitie: str | None = None


GgWithRelations.model_rebuild()
GgWithRelations.model_rebuild()
GgStructWithRelations.model_rebuild()
