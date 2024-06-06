from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Rge(BaseModel):
    notitie: str | None
    re_link: str | None
    rge_cd: int
    tekst: str | None
    titel: str
    ts_mut: datetime
    user_nm: str

    model_config = ConfigDict(from_attributes=True)
