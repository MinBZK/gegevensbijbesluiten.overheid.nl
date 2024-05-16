from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Ond(BaseModel):
    ond_cd: int
    titel: str
    omschrijving: str
    sort_key: int
    notitie: str | None
    ts_mut: datetime
    user_nm: str


class OndIn(BaseModel):
    omschrijving: str
    titel: str
    sort_key: int
    notitie: str | None = None


class OndMinimalList(BaseModel):
    ond_cd: int
    titel: str

    model_config = ConfigDict(from_attributes=True)
