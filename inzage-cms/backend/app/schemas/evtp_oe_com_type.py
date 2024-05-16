from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.schemas.evtp_version import EvtpVersionMinimalList
from app.schemas.oe_com_type import OeComTypeMinimalList


class EvtpOeComType(BaseModel):
    evtp_oe_com_type_cd: int
    evtp_cd: int
    oe_com_type_cd: int
    link: str | None
    user_nm: str
    ts_mut: datetime


class EvtpOeComTypeMinimalList(BaseModel):
    evtp_oe_com_type_cd: int


class EvtpOeComTypeWithRelations(EvtpOeComType):
    entity_evtp_oe_com_type: EvtpVersionMinimalList | None
    entity_oe_com_type: OeComTypeMinimalList | None


class EvtpOeComTypeIn(BaseModel):
    evtp_cd: int
    oe_com_type_cd: int
    link: str | None = None
