from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.schemas.evtp_version import EvtpVersionMinimalList
from app.schemas.ond import OndMinimalList


class EvtpOnd(BaseModel):
    evtp_ond_cd: int
    ond_cd: int
    evtp_cd: int
    notitie: str | None
    ts_mut: datetime
    user_nm: str


class EvtpOndWithRelations(EvtpOnd):
    entity_evtp: EvtpVersionMinimalList
    entity_ond: OndMinimalList


class EvtpOndIn(BaseModel):
    ond_cd: int
    evtp_cd: int
    notitie: str | None = None


class EvtpOndMinimalList(BaseModel):
    evtp_ond_cd: int
