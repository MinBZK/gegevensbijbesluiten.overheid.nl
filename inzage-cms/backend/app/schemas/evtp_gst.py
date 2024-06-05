from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel

from app.schemas.gst import GstMinimalList

if TYPE_CHECKING:  # Fix circular import
    from app.schemas.evtp_version import EvtpVersionMinimalList


class EvtpGst(BaseModel):
    evtp_gst_cd: int
    versie_nr: int
    conditie: str | None
    evtp_cd: int
    gst_cd: int
    notitie: str | None
    sort_key: int | None
    user_nm: str
    ts_mut: datetime
    ts_end: datetime


class EvtpGstMinimalList(BaseModel):
    evtp_gst_cd: int


class EvtpGstWithRelations(EvtpGst):
    entity_gst: GstMinimalList
    entity_evtp_version: EvtpVersionMinimalList


class EvtpGstIn(BaseModel):
    conditie: str | None = None
    evtp_cd: int
    gst_cd: int
    versie_nr: int
    notitie: str | None = None
    sort_key: int | None = None
