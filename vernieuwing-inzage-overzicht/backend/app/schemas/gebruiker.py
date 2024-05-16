from pydantic import BaseModel


class GebruikerBase(BaseModel):
    email: str
    name: str | None


class Gebruiker(GebruikerBase):
    totp: str
    hashed_password: str
