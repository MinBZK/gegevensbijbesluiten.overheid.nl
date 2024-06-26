from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.schemas.evtp_gst import EvtpGstWithRelations
from app.schemas.oe import OeMinimalList


class Evtp(BaseModel):
    evtp_cd: int
    evtp_upc: int


# versions
class EvtpVersion(BaseModel):
    evtp_cd: int
    versie_nr: int
    evtp_cd_sup: int | None
    evtp_nm: str
    omschrijving: str | None
    aanleiding: str | None
    gebr_dl: str | None
    oe_best: int | None
    lidw_soort_besluit: str | None
    soort_besluit: str | None
    uri: str | None
    huidige_versie: bool | str
    id_publicatiestatus: int
    ts_publ: datetime | None
    notitie: str | None
    overige_informatie: str | None = None
    overige_informatie_link: str | None = None
    user_nm: str
    ts_mut: datetime

    @field_validator("huidige_versie", mode="after")
    def replace_boolean_with_string(cls, value) -> Literal["Ja"] | Literal["Nee"]:
        if value is True:
            return "Ja"
        else:
            return "Nee"


class EvtpOeAggregatedStatus(BaseModel):
    index: list[str]
    columns: list[str]
    data: list[list[int]]


class EvtpVersionMinimalList(BaseModel):
    evtp_cd: int
    evtp_nm: str
    versie_nr: int


class EvtpMinimalListIncludingVersions(BaseModel):
    evtp_cd: int
    evtp_nm: str
    versie_nr: int
    id_publicatiestatus: int


class EvtpVersionWithRelations(EvtpVersion):
    verantwoordelijke_oe: OeMinimalList | None
    parent_evtp: ParentEvtp | None


class EvtpVersionIn(BaseModel):
    versie_nr: int | None = Field(..., exclude=True)
    evtp_cd_sup: int | None = None
    evtp_nm: str
    omschrijving: str
    overige_informatie: str | None = None
    overige_informatie_link: str | None = None
    uri: str | None = None
    aanleiding: str
    gebr_dl: str
    oe_best: int
    lidw_soort_besluit: str | None = None
    soort_besluit: str | None = None
    notitie: str | None = None


class EvtpNewVersionIn(BaseModel):
    versie_nr: int
    evtp_cd_sup: int | None = None
    evtp_nm: str
    omschrijving: str
    uri: str | None = None
    aanleiding: str
    gebr_dl: str
    oe_best: int
    lidw_soort_besluit: str | None = None
    soort_besluit: str | None = None
    notitie: str | None = None


class EvtpVersionStatus(BaseModel):
    evtp_cd: int
    versie_nr: int
    evtp_nm: str
    huidige_versie: bool
    id_publicatiestatus: int


# evtp blob class for relations
class ParentEvtp(BaseModel):
    evtp_cd: int
    evtp_nm: str


EvtpVersionWithRelations.model_rebuild()
EvtpGstWithRelations.model_rebuild()
