from pydantic import BaseModel, ConfigDict


class Ond(BaseModel):
    ond_cd: int
    titel: str
    omschrijving: str
    sort_key: int

    model_config = ConfigDict(from_attributes=True)
