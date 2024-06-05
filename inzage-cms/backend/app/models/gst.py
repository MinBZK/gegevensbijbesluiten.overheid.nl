from sqlalchemy import VARCHAR, ForeignKey, Integer
from sqlalchemy.exc import MissingGreenlet
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.models._default_columns import DefaultColumns

from .evtp import EvtpGst


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
        Integer, index=True, comment="Uniforme product code dat hoort bij een gegevensstroom"
    )
    omschrijving: Mapped[str] = mapped_column(VARCHAR(255), comment="Omschrijving van de gegevensstroom")
    oe_bron: Mapped[int] = mapped_column(Integer, ForeignKey("oe.oe_cd"), comment="Organisatorische eenheid bron")
    oe_best: Mapped[int] = mapped_column(Integer, ForeignKey("oe.oe_cd"), comment="Organisatorische eenheid bestemming")
    ibron_cd: Mapped[int | None] = mapped_column(Integer, ForeignKey("ibron.ibron_cd"))
    ext_lnk_aut: Mapped[str | None] = mapped_column(VARCHAR(2000), comment="Hyperlink naar autorisatie")

    # Relationships
    entity_oe_best: Mapped["Oe"] = relationship(  # type: ignore # noqa: F821
        "Oe",
        foreign_keys=[oe_best],
    )

    entity_oe_bron: Mapped["Oe"] = relationship(  # type: ignore # noqa: F821
        "Oe",
        foreign_keys=[oe_bron],
    )
    entity_ibron: Mapped["Ibron"] = relationship("Ibron", foreign_keys=[ibron_cd])  # type: ignore # noqa: F821
    entities_evtp_gst: Mapped[list["EvtpGst"]] = relationship(
        "EvtpGst",
        primaryjoin="and_(Gst.gst_cd == EvtpGst.gst_cd, EvtpGst.ts_end > Gst.ts_start, EvtpGst.ts_start < Gst.ts_end)",
        viewonly=True,
        lazy="selectin",
        back_populates="entity_gst",
    )  # type: ignore # noqa: F821

    @hybrid_property
    def versie_nr(self) -> int | None:
        """
        Gst kan geen versie_nr hebben, maar heeft het nodig om automatisch de koppeltabellen te kunnen genereren vanuit de besluitenboom
        De exception is nodig om circulaire query vanuit EvtpGst.entity_gst af te vangen
        """
        try:
            if not any(self.entities_evtp_gst):
                return
            return max([item.versie_nr for item in self.entities_evtp_gst])

        except MissingGreenlet:
            return


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
        Integer, comment="Versie nummer van de gegevensstroom gegevensstroomtype koppeling"
    )

    # Relationships
    entity_gst_type: Mapped["GstType"] = relationship(
        "GstType",
        foreign_keys=[gstt_cd],
    )
    entity_gst_gstt: Mapped["Gst"] = relationship(
        "Gst",
        foreign_keys=[gst_cd],
        overlaps="entities_gst_gstt",
    )


class GstGg(Base, DefaultColumns):
    """
    Table description: koppeling tussen gegevensstroom en gegevensgroep
    """

    __tablename__ = "gst_gg"
    __table_args__ = {"comment": "Koppeling tussen gegevensstroom en gegevensgroep"}

    gst_gg_cd: Mapped[int] = mapped_column(
        Integer, primary_key=True, comment="Gegevensstroom gegevensgroep regelingelement code"
    )
    gst_cd: Mapped[int] = mapped_column(Integer, ForeignKey("gst.gst_cd"), index=True, comment="Gegevensstroom code")
    gg_cd: Mapped[int] = mapped_column(Integer, ForeignKey("gg.gg_cd"), index=True, comment="Gegevensgroep code")
    versie_nr: Mapped[int] = mapped_column(
        Integer, comment="Versie nummer van de gegevensstroom gegevensgroep koppeling"
    )
    sort_key: Mapped[int | None] = mapped_column(
        Integer, comment="Sorteersleutel van het gegevensgroep in het gegevensstroom blokje"
    )

    # Relationships
    entity_gg: Mapped["Gg"] = relationship("Gg", foreign_keys=[gg_cd])  # type: ignore # noqa: F821
    entity_gst: Mapped["Gst"] = relationship(
        "Gst",
        foreign_keys=[gst_cd],
        overlaps="entities_gst_gg",
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
        Integer, comment="Sorteersleutel van het regelingelement in het gegevensstroom blokje"
    )

    # Relationships
    entity_gst: Mapped["Gst"] = relationship("Gst", foreign_keys=[gst_cd], overlaps="entities_gst_rge")
    entity_rge: Mapped["Rge"] = relationship("Rge", primaryjoin="GstRge.rge_cd == Rge.rge_cd")  # type: ignore # noqa: F821
