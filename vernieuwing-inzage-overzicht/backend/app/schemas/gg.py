from __future__ import annotations

from pydantic import BaseModel

from app.schemas.filters import (
    GgFilterData,
    SelectedFilters,
)


class ChildGgStructuur(BaseModel):
    # parent_gg_entity: ChildGg | None

    class Config:
        from_attributes = True


class ChildGg(BaseModel):
    gg_cd: int
    gg_upc: int
    omschrijving: str
    omschrijving_uitgebreid: str
    sort_key: int | None
    evtp_sort_key: dict | None
    parent_gg_struct: ChildGgStructuur | None

    class Config:
        from_attributes = True


class ParentGgStructuur(BaseModel):
    child_entity: ChildGg | None

    class Config:
        from_attributes = True


class ParentGg(BaseModel):
    gg_cd: int
    omschrijving: str
    omschrijving_uitgebreid: str
    sort_key: int | None
    evtp_sort_key: dict | None
    child_gg_struct: list[ParentGgStructuur] | None

    class Config:
        from_attributes = True


class GgQuery(BaseModel):
    page: int = 1
    limit: int = 10
    searchtext: str | None = None
    organisation: str | None = None


class GgQueryResult(BaseModel):
    results: list[ParentGg]
    total_count: int
    filter_data: GgFilterData
    selected_filters: list[SelectedFilters]


ChildGgStructuur.model_rebuild()
ParentGgStructuur.model_rebuild()
