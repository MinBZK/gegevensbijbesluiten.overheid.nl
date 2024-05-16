from pydantic import BaseModel


# ond
class Ond(BaseModel):
    ond_cd: int
    titel: str
    omschrijving: str
    sort_key: int

    class Config:
        from_attributes = True
