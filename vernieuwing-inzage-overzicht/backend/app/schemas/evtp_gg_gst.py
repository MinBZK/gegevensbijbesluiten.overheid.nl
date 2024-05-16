from typing import List
from urllib.parse import urlparse

from pydantic import (
    BaseModel,
    HttpUrl,
    field_validator,
)


class RgeShort(BaseModel):
    titel: str
    re_link: HttpUrl


class GegevensgroepGrondslag(BaseModel):
    header_oe_best_naamofficieel: str
    gg_child: List[str]
    gg_parent: str
    gg_omschrijvinguitgebreid: List[str]
    oe_best_lidwsgebr: str | None
    oe_best_naampraakgebr: str
    evtp_aanleiding: str
    evtp_gst_conditie: str | None
    evtp_gebrdl: str
    rge: List[RgeShort]


class BronOrganisatie(BaseModel):
    header_oe_bron_naamofficieel: str
    oe_bron_lidwsgebr: str | None
    oe_bron_internetdomein: str | None
    ibron_oe_lidwsgebr: str | None
    ibron_oe_naam_officieel: str | None
    ibron_oe_naam_spraakgbr: str | None
    oe_bron_naampraakgebr: str
    gsttype_gsttoms: List[str]
    ibron_oe_econtact: str | None
    gst_extlnkaut: str | None

    @field_validator("gst_extlnkaut")
    def validate_gst_extlnkaut(cls, value):
        if value and urlparse(value).hostname:
            return value
        return ""


class Besluit(BaseModel):
    evtp_nm: str
    evtp_upc: int


class EvtpGgGst(BaseModel):
    besluit: Besluit
    bron_organisatie: BronOrganisatie
    gegevensgroep_grondslag: GegevensgroepGrondslag
