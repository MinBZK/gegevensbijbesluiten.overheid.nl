from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, HttpUrl, field_validator

from app.schemas.evtp_version import EvtpVersionMinimalList
from app.schemas.oe_com_type import OeComTypeMinimalList
from app.util.misc import validate_url


class EvtpOeComType(BaseModel):
    evtp_oe_com_type_cd: int
    evtp_cd: int
    oe_com_type_cd: int
    versie_nr: int
    link: HttpUrl | None
    user_nm: str
    ts_mut: datetime
    ts_end: datetime


class EvtpOeComTypeMinimalList(BaseModel):
    evtp_oe_com_type_cd: int


class EvtpOeComTypeWithRelations(EvtpOeComType):
    entity_evtp_version_oe_com_type: EvtpVersionMinimalList | None
    entity_oe_com_type: OeComTypeMinimalList | None


class EvtpOeComTypeIn(BaseModel):
    evtp_cd: int
    oe_com_type_cd: int
    versie_nr: int
    link: str | None = None

    _validate_re_link = field_validator("link")(validate_url)
