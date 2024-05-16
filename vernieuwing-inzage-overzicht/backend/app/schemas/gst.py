from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

from app.schemas.oe import (
    Ibron,
    OeRelations,
)
from app.schemas.rge import Rge

if TYPE_CHECKING:  # Fix circular import
    from app.schemas.gg import ChildGg


class GstType(BaseModel):
    gstt_oms: str | None

    class Config:
        from_attributes = True


class GstGstt(BaseModel):
    gst_cd: int
    gstt_cd: int
    entity_gst_type: GstType

    class Config:
        from_attributes = True


class Gst(BaseModel):
    gst_cd: int
    gst_upc: int
    omschrijving: str
    ext_lnk_aut: str | None

    entity_oe_best: OeRelations
    entity_oe_bron: OeRelations
    entity_ibron: Ibron | None
    entities_gst_gstt: list[GstGstt]

    class Config:
        from_attributes = True


class GstGg(BaseModel):
    entity_gg_child: ChildGg | None

    class Config:
        from_attributes = True


class GstRge(BaseModel):
    entity_rge: Rge

    class Config:
        from_attributes = True
