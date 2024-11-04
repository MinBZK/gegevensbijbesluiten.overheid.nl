from pydantic import BaseModel


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
