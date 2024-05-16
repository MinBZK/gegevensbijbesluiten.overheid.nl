from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class Rge(BaseModel):
    notitie: str | None
    re_link: str | None
    rge_cd: int
    tekst: str | None
    titel: str
    ts_mut: datetime
    user_nm: str

    class Config:
        from_attributes = True
