from typing import List

from pydantic import (
    BaseModel,
    HttpUrl,
)


class RgeShort(BaseModel):
    titel: str
    re_link: HttpUrl


class GgChild(BaseModel):
    gg_cd: int
    omschrijving: str
    gg_upc: int


class GegevensgroepGrondslag(BaseModel):
    header_oe_best_naamofficieel: str
    gg_child: List[GgChild]
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
    oe_bron_naampraakgebr: str
    oe_bron_lidwsgebr: str | None
    oe_bron_internetdomein: HttpUrl | None
    ibron_oe_naam_officieel: str | None
    ibron_oe_lidw: str | None
    ibron_titel: str | None
    ibron_lidw: str | None
    ibron_link: HttpUrl | None
    gsttype_gsttoms: List[str]
    gst_extlnkaut: str | None


class Besluit(BaseModel):
    evtp_nm: str
    evtp_upc: int


class EvtpGgGst(BaseModel):
    besluit: Besluit
    bron_organisatie: BronOrganisatie
    gegevensgroep_grondslag: GegevensgroepGrondslag
