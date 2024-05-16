from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.ext.associationproxy import (
    association_proxy,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.database import Base


class Evtp(Base):
    """
    Besluit
    TabelLabelLang: Gebeurtenis ook wel bekend is als besluit
    Comment: Alle unieke besluiten met zijn bijgehorende universele product code nummer
    """

    __tablename__ = "evtp"

    evtp_cd: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    evtp_upc: Mapped[int] = mapped_column(Integer)


class EvtpVersion(Base):
    """
    EvtpVersion
    TabelLabelLang: Versie van een ieder besluit
    Comment: Versie van een ieder besluit met een bepaalde status die aanleiding kunnen zijn voor het
    vastleggen of uitwisselen van gegevensgroepen
    """

    __tablename__ = "evtp_version"

    evtp_cd: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("evtp.evtp_cd"),
        primary_key=True,
    )
    versie_nr: Mapped[int] = mapped_column(Integer, primary_key=True)
    evtp_cd_sup: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("evtp_version.evtp_cd"),
    )
    evtp_nm: Mapped[str] = mapped_column(String)
    aanleiding: Mapped[str] = mapped_column(String)
    gebr_dl: Mapped[str] = mapped_column(String)
    id_publicatiestatus: Mapped[int] = mapped_column(Integer)
    notitie: Mapped[str] = mapped_column(String)
    oe_best: Mapped[int] = mapped_column(Integer, ForeignKey("oe.oe_cd"))
    omschrijving: Mapped[str] = mapped_column(String)
    ts_mut: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    user_nm: Mapped[str] = mapped_column(String)
    lidw_soort_besluit: Mapped[str] = mapped_column(String)
    soort_besluit: Mapped[str] = mapped_column(String)
    uri: Mapped[str | None] = mapped_column(String)
    ts_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ts_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    huidige_versie: Mapped[bool] = mapped_column(Boolean)
    ts_publ: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # Association proxy
    evtp_upc = association_proxy("entity_evtp", "evtp_upc")

    # Relationships
    entity_evtp = relationship("Evtp", foreign_keys=[evtp_cd])
    entity_oe_best = relationship("Oe", foreign_keys=[oe_best])
    entities_evtp_gst = relationship(
        "EvtpGst",
        primaryjoin="and_(EvtpVersion.evtp_cd == EvtpGst.evtp_cd, EvtpVersion.id_publicatiestatus < 4, EvtpVersion.ts_start < EvtpGst.ts_end, EvtpVersion.ts_end > EvtpGst.ts_start)",
        uselist=True,
    )
    entities_evtp_oe_com_type = relationship(
        "EvtpOeComType",
        primaryjoin="and_(EvtpOeComType.evtp_cd == EvtpVersion.evtp_cd, EvtpVersion.ts_start < EvtpOeComType.ts_end, EvtpVersion.ts_end > EvtpOeComType.ts_start)",
        uselist=True,
    )
    entities_evtp_ond = relationship(
        "EvtpOnd",
        primaryjoin="and_(EvtpOnd.evtp_cd == EvtpVersion.evtp_cd, EvtpVersion.ts_start < EvtpOnd.ts_end, EvtpVersion.ts_end > EvtpOnd.ts_start)",
        uselist=True,
    )
