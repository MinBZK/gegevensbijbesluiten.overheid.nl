from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.schemas.evtp_version import EvtpVersionMinimalList
from app.schemas.ond import OndMinimalList


class EvtpOnd(BaseModel):
    evtp_ond_cd: int
    ond_cd: int
    evtp_cd: int
    versie_nr: int
    notitie: str | None
    ts_mut: datetime
    user_nm: str
    ts_end: datetime


class EvtpOndWithRelations(EvtpOnd):
    entity_evtp_version: EvtpVersionMinimalList
    entity_ond: OndMinimalList


class EvtpOndIn(BaseModel):
    ond_cd: int
    evtp_cd: int
    versie_nr: int
    notitie: str | None = None


class EvtpOndMinimalList(BaseModel):
    evtp_ond_cd: int
