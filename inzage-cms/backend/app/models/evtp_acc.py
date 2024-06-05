from datetime import datetime

from sqlalchemy import VARCHAR, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class BestandAcc(Base):
    """
    Table description: de bestanden die horen ter bewijslast voor de accorderingen
    """

    __tablename__ = "bestand_acc"
    __table_args__ = {"comment": "De bestanden die horen ter bewijslast voor de accorderingen"}

    bestand_acc_cd: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Bestandsaccordering code")
    volg_nr: Mapped[int] = mapped_column(Integer, comment="Volgnummer voor meerdere bestanden bij een accordering")
    omschrijving: Mapped[str | None] = mapped_column(VARCHAR(255), comment="Bestandsomschrijving")
    bestand_verwijzing: Mapped[str] = mapped_column(VARCHAR(255), comment="Bestandsverwijzing")
    user_nm: Mapped[str | None] = mapped_column(VARCHAR(30), comment="Gebruikersnaam", server_default="ICTU")
    ts_create: Mapped[datetime] = mapped_column(DateTime(timezone=True), comment="Tijdstip accordering")


class EvtpAcc(Base):
    """
    Table description: accorderingen die gegeven worden door een organisatie op een besluit
    """

    __tablename__ = "evtp_acc"
    __table_args__ = {"comment": "Accorderingen die gegeven worden door een organisatie op een besluit"}

    evtp_acc_cd: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Accordering code")
    evtp_cd: Mapped[int] = mapped_column(Integer, ForeignKey("evtp_version.evtp_cd"), comment="Besluit code")
    oe_cd: Mapped[int] = mapped_column(Integer, ForeignKey("oe.oe_cd"), comment="Organisatie code")
    ts_acc: Mapped[datetime] = mapped_column(DateTime(timezone=True), comment="Tijdstip accordering")
    volg_nr: Mapped[int] = mapped_column(Integer, comment="Volgnummer mocht een accordering uit meerdere bestaan")
    bestand_acc_cd: Mapped[int] = mapped_column(
        Integer, ForeignKey("bestand_acc.bestand_acc_cd"), comment="Bestandsaccordering code"
    )
    notitie: Mapped[str | None] = mapped_column(VARCHAR(4000), comment="Notitieveld")
    user_nm: Mapped[str | None] = mapped_column(VARCHAR(30), comment="Gebruikersnaam", server_default="ICTU")

    entity_evtp_version: Mapped["EvtpVersion"] = relationship(  # type: ignore # noqa: F821
        "EvtpVersion",
        primaryjoin="and_(EvtpVersion.evtp_cd == EvtpAcc.evtp_cd, EvtpVersion.ts_start < EvtpAcc.ts_acc, EvtpVersion.ts_end > EvtpAcc.ts_acc)",
    )
    entity_oe: Mapped["Oe"] = relationship("Oe", foreign_keys=[oe_cd])  # type: ignore # noqa: F821
    entity_bestand: Mapped["BestandAcc"] = relationship("BestandAcc", foreign_keys=[bestand_acc_cd])  # type: ignore # noqa: F821
