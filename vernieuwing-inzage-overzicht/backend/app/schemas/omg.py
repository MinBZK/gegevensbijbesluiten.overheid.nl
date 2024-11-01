from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from app.schemas.oe import (
    OeName,
)


class Omg(BaseModel):
    omg_cd: int
    titel: str
    oe_cd: int
    lidw: str | None
    link: str

    entity_oe: OeName

    model_config = ConfigDict(from_attributes=True)
