from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.schemas.gg import GgMinimalList
from app.schemas.gst import GstMinimalList


class GstGg(BaseModel):
    gst_gg_cd: int
    gg_cd: int
    gst_cd: int
    notitie: str | None
    user_nm: str
    ts_mut: datetime
    sort_key: int | None


class GstGgMinimalList(BaseModel):
    gst_gg_cd: int


class GstGgWithRelations(GstGg):
    entity_gg: GgMinimalList
    entity_gst: GstMinimalList


class GstGgIn(BaseModel):
    gg_cd: int
    gst_cd: int
    notitie: str | None = None
    sort_key: int | None = None
