from pydantic import BaseModel


class FilterData(BaseModel):
    label: str
    key: str
    count: int

    class Config:
        from_attributes = True


class EvtpFilterData(BaseModel):
    organisation: list[FilterData]
    onderwerp: list[FilterData]


class GgFilterData(BaseModel):
    organisation: list[FilterData]
    onderwerp: list[FilterData]


class OeFilterData(BaseModel):
    onderwerp: list[FilterData]


class SelectedFilters(BaseModel):
    key: str
    value: str | None
