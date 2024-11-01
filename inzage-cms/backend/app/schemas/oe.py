from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl, field_validator

from app.schemas.oe_koepel import OeKoepelMinimalList
from app.util.misc import validate_url


# oe
class Oe(BaseModel):
    oe_cd: int
    oe_upc: int
    naam_officieel: str
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


class OeMinimalList(BaseModel):
    oe_cd: int
    naam_officieel: str

    model_config = ConfigDict(from_attributes=True)


class _OeKoepelOeWithRelations(BaseModel):
    parent_entity: OeKoepelMinimalList
    child_entity: OeMinimalList


class OeWithRelations(Oe):
    count_parents: int
    parent_entities: list[_OeKoepelOeWithRelations]


class OeIn(BaseModel):
    afko: str | None = None
    huisnummer: str | None = None
    huisnummer_toev: str | None = None
    internet_domein: str | None = None
    lidw_sgebr: str | None = None
    naam_officieel: str
    naam_spraakgbr: str
    notitie: str | None = None
    plaats: str | None = None
    postcode: str | None = None
    provincie: str | None = None
    straat: str | None = None
    telefoon: str | None = None

    _validate_re_link = field_validator("internet_domein")(validate_url)


OeWithRelations.model_rebuild()
