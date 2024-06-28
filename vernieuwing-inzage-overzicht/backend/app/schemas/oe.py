from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


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
    internet_domein: str | None
    e_contact: str | None
    user_nm: str
    ts_mut: datetime
    ibron_cd: int | None

    model_config = ConfigDict(from_attributes=True)


class OeName(BaseModel):
    naam_spraakgbr: str

    model_config = ConfigDict(from_attributes=True)


class OeQuery(BaseModel):
    page: int = 1
    limit: int = 10
    searchtext: str | None = None
    organisation: str | None = None


class OeQueryResult(BaseModel):
    results: list[OeKoepel]
    total_count_koepel: int
    total_count_underlying: int


class OeRelations(BaseModel):
    naam_spraakgbr: str
    naam_officieel: str
    lidw_sgebr: str | None
    e_contact: str | None
    internet_domein: str | None

    entity_ibron: Ibron | None

    model_config = ConfigDict(from_attributes=True)


class Ibron(BaseModel):
    ibron_cd: int
    omschrijving: str

    entity_oe: OeRelations

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


# class ChildOe(OeBase):
#     parent_oe_struct: OeKoepelOe | None
#     model_config = ConfigDict(from_attributes=True)


# class OeKoepelOe(BaseModel):
#     oe_koepel_oe_cd: int
#     oe_koepel_cd: int
#     oe_cd: int
#     notitie: str | None
#     ts_mut: datetime
#     user_nm: str
#     model_config = ConfigDict(from_attributes=True)


class OeKoepelOe(BaseModel):
    child_entity: OeBase
    # parent_entity: OeKoepel
    model_config = ConfigDict(from_attributes=True)


class OeKoepel(BaseModel):
    titel: str
    omschrijving: str | None
    child_oe_struct: list[OeKoepelOe] | None
    model_config = ConfigDict(from_attributes=True)


OeName.model_rebuild()
OeRelations.model_rebuild()
