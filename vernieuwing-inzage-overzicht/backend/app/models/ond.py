from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.database import Base
from app.models._default_columns import DefaultColumns


class Ond(Base, DefaultColumns):
    """
    Onderwerpen
    TabelLabelLang: Onderwerpen waar entiteiten onder kunnen vallen, zoals besluiten
    Comment: Onderwerpen.
    """

    __tablename__ = "ond"

    ond_cd: Mapped[int] = mapped_column(Integer, primary_key=True)
    titel: Mapped[str] = mapped_column(String)
    omschrijving: Mapped[str] = mapped_column(String)
    sort_key: Mapped[int] = mapped_column(Integer)
    notitie: Mapped[str] = mapped_column(String)
    ts_mut: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    user_nm: Mapped[str] = mapped_column(String)
    ts_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ts_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # Relationships
    entities_ond: Mapped["EvtpOnd"] = relationship(
        "EvtpOnd",
        primaryjoin="EvtpOnd.ond_cd == Ond.ond_cd",
        uselist=False,
    )


class EvtpOnd(Base, DefaultColumns):
    """
    Table description: koppeling tussen besluiten en onderwerpen
    """

    __tablename__ = "evtp_ond"
    __table_args__ = {"comment": "Koppeling tussen onderwerpen en besluiten"}

    evtp_ond_cd: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Onderwerpen besluiten code")
    ond_cd: Mapped[int] = mapped_column(Integer, ForeignKey("ond.ond_cd"), comment="Onderwerp code")
    evtp_cd: Mapped[int] = mapped_column(Integer, ForeignKey("evtp_version.evtp_cd"), comment="Besluit code")
    versie_nr: Mapped[int] = mapped_column(Integer, comment="Versie nummer van de besluit onderwerp koppeling")

    # Relationships
    entity_evtp_version: Mapped["EvtpVersion"] = relationship(  # type: ignore # noqa: F821
        "EvtpVersion",
        primaryjoin="and_(EvtpVersion.evtp_cd == EvtpOnd.evtp_cd, EvtpVersion.ts_start < EvtpOnd.ts_end, EvtpVersion.ts_end > EvtpOnd.ts_start, EvtpOnd.ts_start >= EvtpVersion.ts_start)",
        uselist=True,
        back_populates="entities_evtp_ond",
    )
    entity_ond: Mapped["Ond"] = relationship(
        "Ond",
        foreign_keys=[ond_cd],
        back_populates="entities_ond",
    )
