from pydantic import BaseModel


class Gebruiker(BaseModel):
    email: str
    name: str | None
