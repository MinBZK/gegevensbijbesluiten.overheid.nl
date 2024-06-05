from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.schemas.evtp_version import EvtpVersionMinimalList
from app.schemas.gg import GgMinimalList


class GgEvtpSort(BaseModel):
    gg_evtp_sort_cd: int
    gg_cd: int
    evtp_cd: int
    sort_key: int
    ts_mut: datetime
    user_nm: str


class GgEvtpSortMinimalList(GgEvtpSort):
    gg_evtp_sort_cd: int


class GgEvtpSortWithRelations(GgEvtpSort):
    entity_gg: GgMinimalList
    entity_evtp_version: EvtpVersionMinimalList


class GgEvtpSortIn(BaseModel):
    gg_cd: int
    evtp_cd: int
    sort_key: int


GgEvtpSortWithRelations.model_rebuild()
