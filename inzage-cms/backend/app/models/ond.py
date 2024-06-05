from sqlalchemy import VARCHAR, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.models._default_columns import DefaultColumns


class Ond(Base, DefaultColumns):
    """
    Table description: onderwerpen waar een besluit toebehoort
    """

    __tablename__ = "ond"
    __table_args__ = {"comment": "Onderwerpen waar een besluit toebehoort"}

    ond_cd: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Onderwerp code")
    titel: Mapped[str] = mapped_column(VARCHAR(255), comment="Titel van het onderwerp")
    omschrijving: Mapped[str] = mapped_column(VARCHAR(4000), comment="Omschrijving van het onderwerp")
    sort_key: Mapped[int] = mapped_column(Integer, comment="Sorteer volgorde van het onderwerp")


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
        primaryjoin="and_(EvtpVersion.evtp_cd == EvtpOnd.evtp_cd, EvtpVersion.ts_start < EvtpOnd.ts_end, EvtpVersion.ts_end > EvtpOnd.ts_start)",
    )
    entity_ond: Mapped["Ond"] = relationship(
        "Ond",
        foreign_keys=[ond_cd],
    )
