from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ChildGgStructuur(BaseModel):
    # parent_gg_entity: ChildGg | None

    model_config = ConfigDict(from_attributes=True)


class ChildGg(BaseModel):
    gg_upc: int
    omschrijving: str

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
    searchtext: str | None = None


class GgQueryResult(BaseModel):
    results: list[ParentGg]
    total_count: int


ChildGgStructuur.model_rebuild()
ParentGgStructuur.model_rebuild()
