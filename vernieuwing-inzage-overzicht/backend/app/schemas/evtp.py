from __future__ import annotations

from typing import Dict, List

from pydantic import BaseModel

from app.schemas.filters import (
    EvtpFilterData,
    SelectedFilters,
)
from app.schemas.oe import (
    OeName,
)


class Ond(BaseModel):
    titel: str

    class Config:
        from_attributes = True


class EvtpOnd(BaseModel):
    entity_ond: Ond

    class Config:
        from_attributes = True


class EvtpVersion(BaseModel):
    evtp_cd: int
    evtp_upc: int
    versie_nr: int
    evtp_nm: str
    omschrijving: str | None
    aanleiding: str
    gebr_dl: str
    lidw_soort_besluit: str | None
    soort_besluit: str | None

    entity_oe_best: OeName
    entities_evtp_ond: list[EvtpOnd]

    class Config:
        from_attributes = True


class EvtpVersionForOnd(BaseModel):
    evtp_cd: int
    evtp_upc: int
    versie_nr: int
    evtp_nm: str
    omschrijving: str | None

    class Config:
        from_attributes = True


class EvtpQueryResult(BaseModel):
    results: list[EvtpVersion]
    total_count: int
    filter_data: EvtpFilterData
    selected_filters: list[SelectedFilters]


class EvtpQuery(BaseModel):
    page: int = 1
    limit: int = 10
    searchtext: str | None = None
    organisation: str | None = None


class EvtpOeComType(BaseModel):
    omschrijving: str
    link: str | None


class Gegevensgroep(BaseModel):
    gg_child: list[str]
    oe_best_naamspraakgbr: str
    gst_cd: int
    gst_upc: int
    gg_parent_sort_key: int
    evtp_gst_sort_key: int


class Besluit(BaseModel):
    evtp_cd: int
    evtp_upc: int
    evtp_nm: str
    omschrijving: str
    aanleiding: str
    gebr_dl: str
    soort_besluit: str | None
    lidw_soort_besluit: str | None
    oe_lidw_sgebr: str | None
    oe_naam_spraakgbr: str
    oe_naam_officieel: str
    ond: list[str]


class EvtpCommunication(BaseModel):
    oe_best_econtact: str | None
    evtp_oe_com_type: List[EvtpOeComType] | None
    oe_best_internetdomein: str | None
    evtp_oebest: str


class EvtpGg(BaseModel):
    besluit_communicatie: EvtpCommunication
    besluit: Besluit
    gegevensgroep: Dict[str, list[Gegevensgroep]]
