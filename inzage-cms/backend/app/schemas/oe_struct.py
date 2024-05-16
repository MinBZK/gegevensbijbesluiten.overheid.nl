from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:  # Fix circular import
    from app.schemas.oe import OeMinimalList


class OeStruct(BaseModel):
    oe_struct_cd: int
    oe_cd_sub: int
    oe_cd_sup: int
    koepel: bool | None
    notitie: str | None
    ts_mut: datetime
    user_nm: str


class OeStructMinimalList(BaseModel):
    oe_struct_cd: int
    omschrijving: str


class OeStructWithRelations(OeStruct):
    parent_entity: OeMinimalList
    child_entity: OeMinimalList


class OeStructIn(BaseModel):
    koepel: bool | None = None
    notitie: str | None = None
    oe_cd_sub: int
    oe_cd_sup: int
