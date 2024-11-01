from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ChildGg(BaseModel):
    gg_upc: int
    omschrijving: str
    omschrijving_uitgebreid: str

    model_config = ConfigDict(from_attributes=True)


class ParentGgStructuur(BaseModel):
    child_entity: ChildGg | None

    model_config = ConfigDict(from_attributes=True)


class ParentGg(BaseModel):
    gg_cd: int
    omschrijving: str
    omschrijving_uitgebreid: str
    child_gg_struct: list[ParentGgStructuur] | None = None

    model_config = ConfigDict(from_attributes=True)


class GgQuery(BaseModel):
    page: int = 1
    limit: int = 10
    searchtext: str = ""


class GgQueryResult(BaseModel):
    result_gg: list[ParentGg]
    total_count_koepel: int
    total_count_underlying: int


class GgCompact(BaseModel):
    gg_cd: int
    gg_upc: int


ParentGgStructuur.model_rebuild()
