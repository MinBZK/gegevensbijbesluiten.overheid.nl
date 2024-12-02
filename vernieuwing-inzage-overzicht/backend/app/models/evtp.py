from datetime import datetime
from typing import Optional

from pydantic import HttpUrl
from sqlalchemy import VARCHAR, Boolean, DateTime, ForeignKey, Integer, text
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.ext.associationproxy import (
    association_proxy,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.database import Base
from app.models._default_columns import DefaultColumns


class Evtp(Base):
    """
    Table description: alle unieke besluiten met zijn bijgehorende uniforme product code nummer
    """

    __tablename__ = "evtp"
    __table_args__ = {"comment": "Alle unieke besluiten met zijn bijgehorende uniforme product code nummer"}

    evtp_cd: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="Besluit code")
    evtp_upc: Mapped[int] = mapped_column(
        Integer, index=True, comment="Uniforme product code dat hoort bij een besluit"
    )


class EvtpVersion(Base, DefaultColumns):
    """
    Table description: versie van een ieder besluit met een bepaalde status die aanleiding kunnen zijn voor het
    vastleggen of uitwisselen van gegevensgroepen
    """

    __tablename__ = "evtp_version"
    __table_args__ = {
        "comment": "Versie van een ieder besluit met een bepaalde status die aanleiding kunnen zijn voor het vastleggen of uitwisselen van gegevensgroepen"
    }

    evtp_cd: Mapped[int] = mapped_column(Integer, ForeignKey("evtp.evtp_cd"), primary_key=True, comment="Besluit code")
    versie_nr: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Versie nummer van het besluit")
    evtp_nm: Mapped[str] = mapped_column(VARCHAR(200), comment="Naam van besluit")
    omschrijving: Mapped[str | None] = mapped_column(VARCHAR(2000), comment="Omschrijving het besluit")
    aanleiding: Mapped[str] = mapped_column(VARCHAR(2000), comment="Aanleiding van het nemen van een besluit")
    gebr_dl: Mapped[str] = mapped_column(VARCHAR(200), comment="Gebruiksdoel van het besluit")
    oe_best: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("oe.oe_cd"),
        index=True,
        comment="Verantwoordelijke(=bestemming) organisatie die behoort tot dit besluit",
    )
    omg_cd: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("omg.omg_cd"),
        comment="Omgeving om gerelateerde informatie optie op te kunnen halen",
    )
    lidw_soort_besluit: Mapped[str | None] = mapped_column(VARCHAR(12), comment="Lidwoord van het soort besluit")
    soort_besluit: Mapped[str | None] = mapped_column(
        VARCHAR(50),
        comment="Verschillende soorten officiële besluiten, mededelingen en documenten.",
    )
    uri: Mapped[HttpUrl | None] = mapped_column(VARCHAR(200), comment="Uniform resource identifier voor een besluit")
    huidige_versie: Mapped[bool] = mapped_column(
        Boolean,
        server_default=text("false"),
        comment="Wel of geen huidige versie van besluit",
    )
    id_publicatiestatus: Mapped[int] = mapped_column(Integer, comment="Publicatie nummer voor een besluit")
    ts_publ: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), comment="Tijdstip publicatie")

    overige_informatie: Mapped[str | None] = mapped_column(VARCHAR(4000), comment="Extra informatie over het besluit")
    overige_informatie_link: Mapped[HttpUrl | None] = mapped_column(
        VARCHAR(2000), comment="Link naar extra informatie over het besluit"
    )
    vector: Mapped[str] = mapped_column(TSVECTOR)
    vector_suggestion: Mapped[str] = mapped_column(TSVECTOR)

    # Association proxy
    evtp_upc = association_proxy("entity_evtp", "evtp_upc")

    # Relationships
    entity_evtp: Mapped["Evtp"] = relationship("Evtp", foreign_keys=[evtp_cd])
    entity_oe_best: Mapped["Oe"] = relationship("Oe", foreign_keys=[oe_best])  # type: ignore # noqa: F821
    entities_evtp_gst: Mapped[list["EvtpGst"]] = relationship(
        "EvtpGst",
        primaryjoin="and_(EvtpVersion.evtp_cd == EvtpGst.evtp_cd, EvtpVersion.id_publicatiestatus < 4, EvtpVersion.ts_start < EvtpGst.ts_end, EvtpVersion.ts_end > EvtpGst.ts_start)",
        uselist=True,
    )
    entities_evtp_oe_com_type: Mapped[list["EvtpOeComType"]] = relationship(
        "EvtpOeComType",
        primaryjoin="and_(EvtpOeComType.evtp_cd == EvtpVersion.evtp_cd, EvtpVersion.ts_start < EvtpOeComType.ts_end, EvtpVersion.ts_end > EvtpOeComType.ts_start)",
        uselist=True,
    )
    entities_evtp_ond: Mapped[list["EvtpOnd"]] = relationship(  # type: ignore # noqa: F821
        "EvtpOnd",
        primaryjoin="and_(EvtpOnd.evtp_cd == EvtpVersion.evtp_cd, EvtpVersion.ts_start < EvtpOnd.ts_end, EvtpVersion.ts_end > EvtpOnd.ts_start)",
        uselist=True,
    )
    entity_omg: Mapped[Optional["Omg"]] = relationship("Omg", foreign_keys=[omg_cd])  # type: ignore # noqa: F821


class EvtpGst(Base, DefaultColumns):
    """
    Table description: koppeling tussen een besluit en de gegevensstromen
    """

    __tablename__ = "evtp_gst"
    __table_args__ = {"comment": "Koppeling tussen een besluit en de gegevensstromen"}

    evtp_gst_cd: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Besluit gegevensstroom code")
    evtp_cd: Mapped[int] = mapped_column(Integer, ForeignKey("evtp_version.evtp_cd"), comment="Besluit code")
    gst_cd: Mapped[int] = mapped_column(Integer, ForeignKey("gst.gst_cd"), comment="Gegevensstroom code")
    versie_nr: Mapped[int] = mapped_column(Integer, comment="Versie nummer van de besluit gegevensstroom koppeling ")

    sort_key: Mapped[int | None] = mapped_column(
        Integer,
        comment="Sorteersleutel om de gegevensstromen blokken te ordenen binnen een koepelgegeven van een besluit",
    )

    # Relationships
    entity_gst: Mapped["Gst"] = relationship(  # type: ignore # noqa: F821
        "Gst",
        primaryjoin="EvtpGst.gst_cd == Gst.gst_cd",
        viewonly=True,
    )
    entity_evtp_version: Mapped["EvtpVersion"] = relationship(
        "EvtpVersion",
        primaryjoin="and_(EvtpVersion.evtp_cd == EvtpGst.evtp_cd, EvtpVersion.id_publicatiestatus < 4, EvtpVersion.ts_start < EvtpGst.ts_end, EvtpVersion.ts_end > EvtpGst.ts_start)",
        back_populates="entities_evtp_gst",
    )
    entities_gst_gstt: Mapped[list["GstGstt"]] = relationship(  # type: ignore # noqa: F821
        "GstGstt",
        primaryjoin="and_(EvtpGst.gst_cd == foreign(GstGstt.gst_cd), EvtpGst.ts_start < foreign(GstGstt.ts_end), EvtpGst.ts_end > foreign(GstGstt.ts_start))",
        uselist=True,
    )
    entities_gst_gg: Mapped[list["GstGstt"]] = relationship(  # type: ignore # noqa: F821
        "GstGg",
        primaryjoin="and_(EvtpGst.gst_cd == foreign(GstGg.gst_cd), EvtpGst.ts_start < foreign(GstGg.ts_end), EvtpGst.ts_end >= foreign(GstGg.ts_end))",
        uselist=True,
    )
    entities_gst_rge: Mapped[list["GstRge"]] = relationship(  # type: ignore # noqa: F821
        "GstRge",
        primaryjoin="and_(EvtpGst.gst_cd == foreign(GstRge.gst_cd), EvtpGst.ts_start < foreign(GstRge.ts_end), EvtpGst.ts_end >= foreign(GstRge.ts_end))",
        uselist=True,
    )


class EvtpOeComType(Base, DefaultColumns):
    """
    Table description: koppeling tussen een besluit en bestemmingsorganisatie communicatie kanaal
    """

    __tablename__ = "evtp_oe_com_type"
    __table_args__ = {"comment": "Koppeling tussen een besluit en bestemmingsorganisatie communicatie kanaal"}

    evtp_oe_com_type_cd: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        comment="Besluit bestemmingsorganisatie communicatie kanaal code",
    )
    evtp_cd: Mapped[int] = mapped_column(Integer, ForeignKey("evtp_version.evtp_cd"), comment="Besluit code")
    versie_nr: Mapped[int] = mapped_column(
        Integer,
        comment="Versie nummer van de gegevensstroom bestemmingsorganisatie communicatie koppeling",
    )
    oe_com_type_cd: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("oe_com_type.oe_com_type_cd"),
        comment="Communicatiekanaal type code",
    )
    link: Mapped[HttpUrl | None] = mapped_column(
        VARCHAR(2000),
        comment="Hyperlink waar de burger de uitkomst van het besluit ontvangt",
    )

    # Relationships
    entity_oe_com_type: Mapped["EvtpVersion"] = relationship(
        "OeComType",
        foreign_keys=[oe_com_type_cd],
    )


class Omg(Base, DefaultColumns):
    """
    Table description: Omgeving van de organisatie waar relevante informatie gevonden kan worden
    """

    __tablename__ = "omg"
    __table_args__ = {"comment": "Omgeving van de organisatie waar informatie gevonden kan worden"}

    omg_cd: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Omgeving code")
    titel: Mapped[str] = mapped_column(VARCHAR(255), comment="Naam van de omgeving")
    oe_cd: Mapped[int] = mapped_column(Integer, ForeignKey("oe.oe_cd"), comment="Gerelateerde organisatie code")
    lidw: Mapped[str | None] = mapped_column(VARCHAR(12), comment="Lidwoord")
    link: Mapped[HttpUrl] = mapped_column(VARCHAR(2000), comment="Hyperlink naar omgeving")
    entity_oe: Mapped["Oe"] = relationship("Oe", foreign_keys=[oe_cd])  # type: ignore # noqa: F821
