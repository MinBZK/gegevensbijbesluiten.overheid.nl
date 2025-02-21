from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl

from app.schemas.evtp_ond import OndMinimalList
from app.schemas.oe_com_type import OeComTypeMinimalList
from app.schemas.oe_koepel_oe import OeKoepelOe, OeKoepelOeWithRelations
from app.schemas.omg import OmgMinimalList


# Base classes, have no relations
class OeBase(BaseModel):
    oe_cd: int
    naam_officieel: str
    lidw_sgebr: str | None
    naam_spraakgbr: str

    model_config = ConfigDict(from_attributes=True)


class EvtpOndBase(BaseModel):
    evtp_ond_cd: int
    ond_cd: int
    evtp_cd: int

    entity_ond: OndMinimalList

    model_config = ConfigDict(from_attributes=True)


class IbronBase(BaseModel):
    ibron_cd: int
    titel: str
    afko: str | None
    lidw: str | None
    link: HttpUrl | None
    oe_cd: int | None
    user_nm: str
    notitie: str | None
    ts_mut: datetime

    model_config = ConfigDict(from_attributes=True)


class IbronWithRelations(IbronBase):
    entity_oe: OeBase | None

    model_config = ConfigDict(from_attributes=True)


class OeWithRelations(OeBase):
    parent_entities: list[OeKoepelOe]
    count_parents: int

    model_config = ConfigDict(from_attributes=True)


class OeWithNestedRelations(OeWithRelations):
    parent_entities: list[OeKoepelOeWithRelations]

    model_config = ConfigDict(from_attributes=True)


class GgBase(BaseModel):
    gg_cd: int
    omschrijving: str
    notitie: str | None
    omschrijving_uitgebreid: str

    model_config = ConfigDict(from_attributes=True)


class GgStruct(BaseModel):
    gg_struct_cd: int
    gg_cd_sub: int
    gg_cd_sup: int
    notitie: str | None
    ts_mut: datetime
    user_nm: str

    model_config = ConfigDict(from_attributes=True)


class GgStructWithRelations(GgStruct):
    parent_entity: GgBase
    child_entity: GgBase


class GgWithRelationCount(GgBase):
    count_parents: int
    count_children: int


class GgWithParentsChildren(GgWithRelationCount):
    parent_entities: list[GgStructWithRelations]
    child_entities: list[GgStructWithRelations]


class RgeBase(BaseModel):
    rge_cd: int
    titel: str
    re_link: str | None

    model_config = ConfigDict(from_attributes=True)


class GstTypeBase(BaseModel):
    gstt_cd: int
    gstt_naam: str
    gstt_oms: str | None
    ts_mut: datetime
    user_nm: str
    gstt_pp: str | None

    model_config = ConfigDict(from_attributes=True)


class GstGsttBase(BaseModel):
    gst_cd: int
    gstt_cd: int
    gst_gstt_cd: int
    entity_gst_type: GstTypeBase

    model_config = ConfigDict(from_attributes=True)


class EvtpOeComType(BaseModel):
    evtp_oe_com_type_cd: int
    oe_com_type_cd: int
    entity_oe_com_type: OeComTypeMinimalList

    model_config = ConfigDict(from_attributes=True)


# Relational classes
class GstGgTreeStructure(BaseModel):
    gst_gg_cd: int
    sort_key: int | None
    entity_gg: GgWithParentsChildren | None

    model_config = ConfigDict(from_attributes=True)


class GstRgeTreeStructure(BaseModel):
    gst_rge_cd: int
    sort_key: int | None
    entity_rge: RgeBase | None

    model_config = ConfigDict(from_attributes=True)


class EvtpGstVersion(BaseModel):
    ts_start: datetime


class GstTreeStructure(BaseModel):
    gst_cd: int
    oe_bron: int
    oe_best: int
    omschrijving: str
    conditie: str | None

    entity_oe_best: OeWithNestedRelations | None
    entity_oe_bron: OeWithNestedRelations | None
    entity_ibron: IbronWithRelations | None

    model_config = ConfigDict(from_attributes=True)


class EvtpGstTreeStructure(BaseModel):
    evtp_gst_cd: int
    evtp_cd: int
    gst_cd: int
    notitie: str | None
    sort_key: int | None

    entity_gst: GstTreeStructure | None
    entities_gst_gstt: list[GstGsttBase] | None
    entities_gst_gg: list[GstGgTreeStructure] | None
    entities_gst_rge: list[GstRgeTreeStructure] | None

    model_config = ConfigDict(from_attributes=True)


# Event type structure (with parent and optional child entities)
class EvtpStructure(BaseModel):
    evtp_cd: int

    model_config = ConfigDict(from_attributes=True)


class EvtpTreeStructure(BaseModel):
    evtp_cd: int
    versie_nr: int
    evtp_nm: str
    oe_best: int | None
    gebr_dl: str | None
    aanleiding: str | None
    id_publicatiestatus: int
    huidige_versie: bool
    omschrijving: str

    verantwoordelijke_oe: OeWithNestedRelations
    entities_evtp_gst: list[EvtpGstTreeStructure] | None
    entities_evtp_oe_com_type: list[EvtpOeComType] | None
    entities_evtp_ond: list[EvtpOndBase] | None
    entity_omg: OmgMinimalList | None

    model_config = ConfigDict(from_attributes=True)
