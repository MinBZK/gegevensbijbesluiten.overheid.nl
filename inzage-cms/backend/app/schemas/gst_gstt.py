from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.schemas.gst import GstMinimalList
from app.schemas.gst_type import GstTypeMinimalList


class GstGstt(BaseModel):
    gst_gstt_cd: int
    gst_cd: int
    gstt_cd: int
    notitie: str | None
    user_nm: str
    ts_mut: datetime


class GstGsttMinimalList(BaseModel):
    gst_gstt_cd: int


class GstGsttWithRelations(GstGstt):
    entity_gsttype: GstTypeMinimalList
    entity_gst_gstt: GstMinimalList


class GstGsttIn(BaseModel):
    gst_cd: int
    gstt_cd: int
    notitie: str | None = None
