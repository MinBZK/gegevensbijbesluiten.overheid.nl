from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.schemas.gst import GstMinimalList
from app.schemas.rge import RgeMinimalList


class GstRge(BaseModel):
    gst_rge_cd: int
    rge_cd: int
    versie_nr: int
    notitie: str | None
    user_nm: str
    sort_key: int | None
    ts_mut: datetime
    ts_end: datetime


class GstRgeMinimalList(BaseModel):
    gst_rge_cd: int


class GstRgeWithRelations(GstRge):
    entity_gst: GstMinimalList
    entity_rge: RgeMinimalList


class GstRgeIn(BaseModel):
    gst_cd: int
    rge_cd: int
    versie_nr: int
    notitie: str | None = None
    sort_key: int | None = None
