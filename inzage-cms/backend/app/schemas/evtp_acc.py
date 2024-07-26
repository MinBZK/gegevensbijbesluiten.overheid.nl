from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.schemas.evtp_version import EvtpVersionMinimalList
from app.schemas.oe import OeMinimalList


class BestandAcc(BaseModel):
    bestand_acc_cd: int | None
    volg_nr: int | None
    omschrijving: str | None
    bestand_verwijzing: str | None
    ts_create: datetime | None
    user_nm: str


# Evtp Accorderingen en Bestand Accorderingen
class EvtpAcc(BaseModel):
    evtp_acc_cd: int
    evtp_cd: int
    oe_cd: int
    ts_acc: datetime
    notitie: str | None
    volg_nr: int | None
    bestand_acc_cd: int
    user_nm: str


class EvtpAccMinimalList(BaseModel):
    evtp_acc_cd: int


class EvtpAccIn(BaseModel):
    evtp_cd: int
    oe_cd: int | None = None  # automatically filled
    notitie: str
    volg_nr: int | None = None


class EvtpAccWithRelations(EvtpAcc):
    entity_evtp_version: EvtpVersionMinimalList
    entity_oe: OeMinimalList
    entity_bestand: BestandAcc | None
