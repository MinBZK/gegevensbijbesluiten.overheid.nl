from pydantic import BaseModel, ConfigDict


class FilterData(BaseModel):
    label: str
    key: str
    count: int

    model_config = ConfigDict(from_attributes=True)


class EvtpFilterData(BaseModel):
    organisation: list[FilterData]


class GgFilterData(BaseModel):
    organisation: list[FilterData]


class SelectedFilters(BaseModel):
    key: str
    value: str | None
