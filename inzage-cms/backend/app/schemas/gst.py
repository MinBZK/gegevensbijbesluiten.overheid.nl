from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.schemas.ibron import IbronMinimalList
from app.schemas.oe import OeMinimalList


class Gst(BaseModel):
    gst_cd: int
    gst_upc: int
    versie_nr: int | None = None
    ext_lnk_aut: str | None
    ibron_cd: int | None
    notitie: str | None
    oe_best: int
    oe_bron: int
    omschrijving: str
    ts_mut: datetime
    user_nm: str


class GstMinimalList(BaseModel):
    gst_cd: int
    versie_nr: int | None = None
    omschrijving: str


class GstWithRelations(Gst):
    entity_ibron: IbronMinimalList | None
    entity_oe_best: OeMinimalList
    entity_oe_bron: OeMinimalList


class GstIn(BaseModel):
    ext_lnk_aut: str | None = None
    ibron_cd: int | None = None
    notitie: str | None = None
    oe_best: int
    oe_bron: int
    omschrijving: str


GstWithRelations.model_rebuild()
