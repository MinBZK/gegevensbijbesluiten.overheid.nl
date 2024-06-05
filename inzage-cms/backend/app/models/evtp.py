from datetime import datetime

from sqlalchemy import VARCHAR, Boolean, DateTime, ForeignKey, Integer, text
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
    evtp_cd_sup: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("evtp_version.evtp_cd"), comment="Koepelbesluit"
    )
    evtp_nm: Mapped[str] = mapped_column(VARCHAR(200), comment="Naam van besluit")
    omschrijving: Mapped[str | None] = mapped_column(VARCHAR(2000), comment="Omschrijving het besluit")

    overige_informatie: Mapped[str | None] = mapped_column(VARCHAR(4000), comment="Extra informatie over het besluit")
    overige_informatie_link: Mapped[str | None] = mapped_column(
        VARCHAR(2000), comment="Link naar extra informatie over het besluit"
    )

    aanleiding: Mapped[str] = mapped_column(VARCHAR(2000), comment="Aanleiding van het nemen van een besluit")
    gebr_dl: Mapped[str] = mapped_column(VARCHAR(200), comment="Gebruiksdoel van het besluit")
    oe_best: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("oe.oe_cd"),
        index=True,
        comment="Verantwoordelijke(=bestemming) organisatie die behoort tot dit besluit",
    )
    lidw_soort_besluit: Mapped[str | None] = mapped_column(VARCHAR(12), comment="Lidwoord van het soort besluit")
    soort_besluit: Mapped[str | None] = mapped_column(
        VARCHAR(50),
        comment="Verschillende soorten officiële besluiten, mededelingen en documenten.",
    )
    uri: Mapped[str | None] = mapped_column(VARCHAR(200), comment="Uniform resource identifier voor een besluit")
    huidige_versie: Mapped[bool] = mapped_column(
        Boolean, server_default=text("false"), comment="Wel of geen huidige versie van besluit"
    )
    id_publicatiestatus: Mapped[int] = mapped_column(Integer, comment="Publicatie nummer voor een besluit")
    ts_publ: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), comment="Tijdstip publicatie")

    # Association proxy
    evtp_upc = association_proxy("entity_evtp_version", "evtp_upc")

    # Relationships
    verantwoordelijke_oe: Mapped["Oe"] = relationship("Oe", foreign_keys=[oe_best])  # type: ignore # type: ignore # noqa: F821
    parent_evtp: Mapped["EvtpVersion"] = relationship(
        "EvtpVersion",
        primaryjoin="and_(EvtpVersion.evtp_cd_sup == remote(EvtpVersion.evtp_cd), remote(EvtpVersion.ts_start) < func.now(), remote(EvtpVersion.ts_end) > func.now())",
        remote_side=[evtp_cd],
        viewonly=True,
    )
    entities_evtp_gst: Mapped[list["EvtpGst"]] = relationship(
        "EvtpGst",
        primaryjoin="and_(EvtpVersion.evtp_cd == EvtpGst.evtp_cd, EvtpVersion.id_publicatiestatus < 4, EvtpVersion.ts_start < EvtpGst.ts_end, EvtpVersion.ts_end > EvtpGst.ts_start)",
        back_populates="entity_evtp_version",
    )
    entities_evtp_oe_com_type: Mapped[list["EvtpOeComType"]] = relationship(
        "EvtpOeComType",
        primaryjoin="and_(EvtpVersion.evtp_cd == EvtpOeComType.evtp_cd, EvtpVersion.ts_start < EvtpOeComType.ts_end, EvtpVersion.ts_end > EvtpOeComType.ts_start)",
        back_populates="entity_evtp_version_oe_com_type",
    )
    entities_evtp_ond: Mapped[list["EvtpOnd"]] = relationship(  # type: ignore # type: ignore # noqa: F821
        "EvtpOnd",
        primaryjoin="and_(EvtpVersion.evtp_cd == EvtpOnd.evtp_cd, EvtpVersion.ts_start < EvtpOnd.ts_end, EvtpVersion.ts_end > EvtpOnd.ts_start)",
        back_populates="entity_evtp_version",
    )

    @hybrid_property
    def count_evtp_gst(self) -> int:
        return len(self.entities_evtp_gst)


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
    conditie: Mapped[str | None] = mapped_column(
        VARCHAR(4000),
        comment="Toelichting van een conditie waaronder de gegevensstroom plaatsvindt, bijvoorbeeld ziek worden, wel of geen werk hebben, etc.",
    )
    sort_key: Mapped[int | None] = mapped_column(
        Integer,
        comment="Sorteersleutel om de gegevensstromen blokken te ordenen binnen een koepelgegeven van een besluit",
    )

    # Relationships
    entity_gst: Mapped["Gst"] = relationship(  # type: ignore # noqa: F821
        "Gst",
        primaryjoin="EvtpGst.gst_cd == Gst.gst_cd",
    )
    entity_evtp_version: Mapped["EvtpVersion"] = relationship(
        "EvtpVersion",
        primaryjoin="and_(EvtpVersion.evtp_cd == EvtpGst.evtp_cd, EvtpVersion.ts_start < EvtpGst.ts_end, EvtpVersion.ts_end > EvtpGst.ts_start)",
        back_populates="entities_evtp_gst",
    )
    entities_gst_gstt: Mapped[list["GstGstt"]] = relationship(  # type: ignore # noqa: F821
        "GstGstt",
        primaryjoin="and_(EvtpGst.gst_cd == foreign(GstGstt.gst_cd), GstGstt.ts_end > EvtpGst.ts_start, GstGstt.ts_start < EvtpGst.ts_end)",
        viewonly=True,
    )
    entities_gst_gg: Mapped[list["GstGg"]] = relationship(  # type: ignore # noqa: F821
        "GstGg",
        primaryjoin="and_(EvtpGst.gst_cd == foreign(GstGg.gst_cd), EvtpGst.ts_start < foreign(GstGg.ts_end), EvtpGst.ts_end > foreign(GstGg.ts_start))",
        viewonly=True,
    )
    entities_gst_rge: Mapped[list["GstRge"]] = relationship(  # type: ignore # noqa: F821
        "GstRge",
        primaryjoin="and_(EvtpGst.gst_cd == foreign(GstRge.gst_cd), EvtpGst.ts_start < foreign(GstRge.ts_end), EvtpGst.ts_end > foreign(GstRge.ts_start))",
        viewonly=True,
    )


class EvtpOeComType(Base, DefaultColumns):
    """
    Table description: koppeling tussen een besluit en bestemmingsorganisatie communicatie kanaal
    """

    __tablename__ = "evtp_oe_com_type"
    __table_args__ = {"comment": "Koppeling tussen een besluit en bestemmingsorganisatie communicatie kanaal"}

    evtp_oe_com_type_cd: Mapped[int] = mapped_column(
        Integer, primary_key=True, comment="Besluit bestemmingsorganisatie communicatie kanaal code"
    )
    evtp_cd: Mapped[int] = mapped_column(Integer, ForeignKey("evtp_version.evtp_cd"), comment="Besluit code")
    versie_nr: Mapped[int] = mapped_column(
        Integer, comment="Versie nummer van de gegevensstroom bestemmingsorganisatie communicatie koppeling"
    )
    oe_com_type_cd: Mapped[int] = mapped_column(
        Integer, ForeignKey("oe_com_type.oe_com_type_cd"), comment="Communicatiekanaal type code"
    )
    link: Mapped[str | None] = mapped_column(
        VARCHAR(2000), comment="Hyperlink waar de burger de uitkomst van het besluit ontvangt"
    )

    # Relationships
    entity_evtp_version_oe_com_type: Mapped["EvtpVersion"] = relationship(
        "EvtpVersion",
        primaryjoin="and_(EvtpVersion.evtp_cd == EvtpOeComType.evtp_cd, EvtpVersion.ts_start < EvtpOeComType.ts_end, EvtpVersion.ts_end > EvtpOeComType.ts_start)",
    )
    entity_oe_com_type: Mapped["OeComType"] = relationship(  # type: ignore # noqa: F821
        "OeComType",
        foreign_keys=[oe_com_type_cd],
    )
