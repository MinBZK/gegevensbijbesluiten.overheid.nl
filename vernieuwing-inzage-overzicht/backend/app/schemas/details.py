from __future__ import annotations

from pydantic import BaseModel

from app.schemas import (
    ChildGg,
    EvtpVersion,
    Oe,
)


class OeDetails(BaseModel):
    oe: Oe
    evtpManaged: list[EvtpVersion]
    ggManaged: list[ChildGg]
    ggReceive: list[ChildGg]


class GgDetails(BaseModel):
    gg: ChildGg
    evtp: list[EvtpVersion]
    oe_best: list[Oe]
    oe_bron: list[Oe]
