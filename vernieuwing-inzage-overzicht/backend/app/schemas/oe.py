from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl


class Oe(BaseModel):
    oe_cd: int
    oe_upc: int
    naam_officieel: str | None
    naam_spraakgbr: str
    afko: str | None
    lidw_sgebr: str | None
    notitie: str | None
    straat: str | None
    huisnummer: str | None
    huisnummer_toev: str | None
    postcode: str | None
    plaats: str | None
    provincie: str | None
    telefoon: str | None
    internet_domein: HttpUrl | None
    user_nm: str
    ts_mut: datetime

    model_config = ConfigDict(from_attributes=True)


class OeName(BaseModel):
    naam_spraakgbr: str
    lidw_sgebr: str | None

    model_config = ConfigDict(from_attributes=True)


class OeQuery(BaseModel):
    page: int = 1
    limit: int = 10
    searchtext: str = ""
    organisation: str | None = None


class OeQueryResult(BaseModel):
    result_oe: list[OeKoepel]
    total_count_koepel: int
    total_count_underlying: int


class OeRelations(BaseModel):
    naam_spraakgbr: str
    naam_officieel: str
    lidw_sgebr: str | None
    internet_domein: str | None

    model_config = ConfigDict(from_attributes=True)


class OeByEvtp(BaseModel):
    naam_officieel: str
    count: int


class OeByEvtpTotal(BaseModel):
    oe_by_evtp_total: list[OeByEvtp]


class OeBase(BaseModel):
    oe_upc: int
    naam_officieel: str | None
    model_config = ConfigDict(from_attributes=True)


class OeKoepelOe(BaseModel):
    child_entity: OeBase
    model_config = ConfigDict(from_attributes=True)


class OeKoepel(BaseModel):
    titel: str
    omschrijving: str | None
    child_oe_struct: list[OeKoepelOe] | None
    model_config = ConfigDict(from_attributes=True)


OeName.model_rebuild()
OeRelations.model_rebuild()
