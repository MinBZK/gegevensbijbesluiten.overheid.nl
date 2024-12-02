from sqlalchemy import VARCHAR, ForeignKey, Integer
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.database import Base
from app.models._default_columns import DefaultColumns


class Gst(Base, DefaultColumns):
    """
    Table description: gegevensstroom die tussen bron- en bestemmingsorganisatorische eenheden loopt waarbij gegevensgroepen worden gedeeld
    """

    __tablename__ = "gst"
    __table_args__ = {
        "comment": "Gegevensstroom die tussen bron- en bestemmingsorganisatorische eenheden loopt waarbij gegevensgroepen worden gedeeld"
    }

    gst_cd: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Gegevensstroom code")
    gst_upc: Mapped[int] = mapped_column(
        Integer,
        index=True,
        comment="Uniforme product code dat hoort bij een gegevensstroom",
    )
    omschrijving: Mapped[str] = mapped_column(VARCHAR(255), comment="Omschrijving van de gegevensstroom")
    oe_bron: Mapped[int] = mapped_column(Integer, ForeignKey("oe.oe_cd"), comment="Organisatorische eenheid bron")
    oe_best: Mapped[int] = mapped_column(Integer, ForeignKey("oe.oe_cd"), comment="Organisatorische eenheid bestemming")
    ibron_cd: Mapped[int | None] = mapped_column(Integer, ForeignKey("ibron.ibron_cd"))
    ext_lnk_aut: Mapped[str | None] = mapped_column(VARCHAR(2000), comment="Hyperlink naar autorisatie")
    conditie: Mapped[str | None] = mapped_column(
        VARCHAR(4000),
        comment="Toelichting van een conditie waaronder de gegevensstroom plaatsvindt, bijvoorbeeld ziek worden, wel of geen werk hebben, etc.",
    )

    # Relationships
    entity_oe_best: Mapped["Oe"] = relationship(  # type: ignore # noqa: F821
        "Oe",
        foreign_keys=[oe_best],
    )
    entity_oe_bron: Mapped["Oe"] = relationship(  # type: ignore # noqa: F821
        "Oe",
        foreign_keys=[oe_bron],
    )
    entity_ibron: Mapped["Ibron"] = relationship(  # type: ignore # noqa: F821
        "Ibron",
        foreign_keys=[ibron_cd],
    )


class GstType(Base, DefaultColumns):
    """
    Table description: type gegevensstroom
    """

    __tablename__ = "gst_type"
    __table_args__ = {"comment": "Type gegevensstroom"}

    gstt_cd: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Gegevensstroomtype code")
    gstt_naam: Mapped[str] = mapped_column(VARCHAR(200), comment="Naam van het soort stroom")
    gstt_oms: Mapped[str] = mapped_column(VARCHAR(2000), comment="Kort omschrijving van de gegevensstroom")
    gstt_pp: Mapped[str | None] = mapped_column(VARCHAR(20), comment="Push of pull van een gegevenstroom type")


class GstGstt(Base, DefaultColumns):
    """
    Table description: koppeling tussen gegevensstroom en gegevensstroomtype
    """

    __tablename__ = "gst_gstt"
    __table_args__ = {"comment": "Koppeling tussen gegevensstroom en gegevensstroomtype"}

    gst_gstt_cd: Mapped[int] = mapped_column(
        Integer, primary_key=True, comment="Gegevensstroom gegevensstroomtype code"
    )
    gstt_cd: Mapped[int] = mapped_column(Integer, ForeignKey("gst_type.gstt_cd"), comment="Gegevensstroomtype code")
    gst_cd: Mapped[int] = mapped_column(Integer, ForeignKey("gst.gst_cd"), comment="Gegevensstroom code")
    versie_nr: Mapped[int] = mapped_column(
        Integer,
        comment="Versie nummer van de gegevensstroom gegevensstroomtype koppeling",
    )

    # Relationships
    entity_gst_type: Mapped["GstType"] = relationship(
        "GstType",
        foreign_keys=[gstt_cd],
    )


class GstGg(Base, DefaultColumns):
    """
    Table description: koppeling tussen gegevensstroom en gegevensgroep
    """

    __tablename__ = "gst_gg"
    __table_args__ = {"comment": "Koppeling tussen gegevensstroom en gegevensgroep"}

    gst_gg_cd: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        comment="Gegevensstroom gegevensgroep regelingelement code",
    )
    gst_cd: Mapped[int] = mapped_column(Integer, ForeignKey("gst.gst_cd"), index=True, comment="Gegevensstroom code")
    gg_cd: Mapped[int] = mapped_column(Integer, ForeignKey("gg.gg_cd"), index=True, comment="Gegevensgroep code")
    versie_nr: Mapped[int] = mapped_column(
        Integer, comment="Versie nummer van de gegevensstroom gegevensgroep koppeling"
    )
    sort_key: Mapped[int | None] = mapped_column(
        Integer,
        comment="Sorteersleutel van het gegevensgroep in het gegevensstroom blokje",
    )

    # Relationships
    entity_gg_child: Mapped["Gg"] = relationship(  # type: ignore # noqa: F821
        "Gg", foreign_keys=[gg_cd], viewonly=True
    )


class GstRge(Base, DefaultColumns):
    """
    Table description: koppeling tussen gegevensstroom en regelingelement
    """

    __tablename__ = "gst_rge"
    __table_args__ = {"comment": "Koppeling tussen gegevensstroom en regelingelement"}

    gst_rge_cd: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Gegevensstroom regelingelement code")
    gst_cd: Mapped[int] = mapped_column(Integer, ForeignKey("gst.gst_cd"), index=True, comment="Gegevensstroom code")
    rge_cd: Mapped[int] = mapped_column(Integer, ForeignKey("rge.rge_cd"), index=True, comment="Regelingelement code")
    versie_nr: Mapped[int] = mapped_column(Integer, comment="Versie nummer van de gegevensstroom regeling koppeling")
    sort_key: Mapped[int | None] = mapped_column(
        Integer,
        comment="Sorteersleutel van het regelingelement in het gegevensstroom blokje",
    )

    # Relationships
    entity_rge: Mapped["Rge"] = relationship(  # type: ignore # noqa: F821
        "Rge",
        primaryjoin="Rge.rge_cd == GstRge.rge_cd",
    )
