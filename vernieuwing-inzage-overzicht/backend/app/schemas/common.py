from pydantic import BaseModel, computed_field


class ChildParentPair(BaseModel):
    parent_cd: int
    child_cd: int


class SearchSuggestion(BaseModel):
    title: str
    version: int | None
    upc: int


class SearchSuggestionsAllEntities(BaseModel):
    evtp: list[SearchSuggestion] | None
    gg: list[SearchSuggestion] | None
    oe: list[SearchSuggestion] | None

    @computed_field
    @property
    def total_count(self) -> int:
        return len(self.evtp or []) + len(self.gg or []) + len(self.oe or [])
