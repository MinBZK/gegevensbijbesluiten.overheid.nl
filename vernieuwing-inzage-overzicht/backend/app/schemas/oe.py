from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.schemas.filters import (
    OeFilterData,
    SelectedFilters,
)


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

    class Config:
        from_attributes = True


class OeName(BaseModel):
    naam_spraakgbr: str

    class Config:
        from_attributes = True


class OeQuery(BaseModel):
    page: int = 1
    limit: int = 10
    searchtext: str | None = None
    organisation: str | None = None


class OeQueryResult(BaseModel):
    results: list[ParentOe]
    total_count: int
    filter_data: OeFilterData
    selected_filters: list[SelectedFilters]


class OeRelations(BaseModel):
    naam_spraakgbr: str
    naam_officieel: str
    lidw_sgebr: str | None
    e_contact: str | None
    internet_domein: str | None

    entity_ibron: Ibron | None

    class Config:
        from_attributes = True


class Ibron(BaseModel):
    ibron_cd: int
    omschrijving: str

    entity_oe: OeRelations

    class Config:
        from_attributes = True


class OeByEvtp(BaseModel):
    naam_officieel: str
    count: int


class OeByEvtpTotal(BaseModel):
    oe_by_evtp_total: list[OeByEvtp]


class OeBase(BaseModel):
    oe_cd: int
    oe_upc: int
    naam_officieel: str | None
    naam_spraakgbr: str


class ChildOeStructuur(BaseModel):
    # parent_gg_entity: ChildGg | None

    class Config:
        from_attributes = True


class ChildOe(OeBase):
    parent_oe_struct: ChildOeStructuur | None

    class Config:
        from_attributes = True


class ParentOeStructuur(BaseModel):
    child_entity: ChildOe | None

    class Config:
        from_attributes = True


class ParentOe(OeBase):
    child_oe_struct: list[ParentOeStructuur] | None

    class Config:
        from_attributes = True


OeName.model_rebuild()
OeRelations.model_rebuild()
