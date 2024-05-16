from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class GstType(BaseModel):
    gstt_cd: int
    gstt_naam: str
    gstt_oms: str | None
    notitie: str | None
    ts_mut: datetime
    user_nm: str
    gstt_pp: str | None


class GstTypeMinimalList(BaseModel):
    gstt_cd: int
    gstt_naam: str


class GstTypeIn(BaseModel):
    gstt_naam: str
    gstt_oms: str
    gstt_pp: str | None = None
    notitie: str | None = None
