from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:  # Fix circular import
    from app.schemas.gg import GgMinimalList


class GgStruct(BaseModel):
    gg_struct_cd: int
    gg_cd_sub: int
    gg_cd_sup: int
    notitie: str | None
    ts_mut: datetime
    user_nm: str


class GgStructMinimalList(BaseModel):
    gg_struct_cd: int


class GgStructWithRelations(GgStruct):
    parent_entity: GgMinimalList
    child_entity: GgMinimalList


class GgStructIn(BaseModel):
    gg_cd_sub: int
    gg_cd_sup: int
    notitie: str | None = None
