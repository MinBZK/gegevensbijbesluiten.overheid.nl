from sqlalchemy import VARCHAR, ForeignKey, Integer
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.models._default_columns import DefaultColumns


class Oe(Base, DefaultColumns):
    """
    Table description: organisatorische eenheid en of instantie
    """

    __tablename__ = "oe"
    __table_args__ = {"comment": "Organisatorische eenheid en of instantie"}

    oe_cd: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        comment="Organisatie code",
    )
    oe_upc: Mapped[int] = mapped_column(Integer)

    afko: Mapped[str | None] = mapped_column(VARCHAR(15), comment="Afkorting van de organisatorische eenheid")
    e_contact: Mapped[str | None] = mapped_column(
        VARCHAR(200),
        comment="E-mail contactadres - indien alleen een prefix is opgenomen wordt de domeinnaam ge-append",
    )
    huisnummer: Mapped[str | None] = mapped_column(VARCHAR(10), comment="Huisnummer")
    huisnummer_toev: Mapped[str | None] = mapped_column(VARCHAR(10), comment="Huisnummer toevoeging")
    ibron_cd: Mapped[int | None] = mapped_column(Integer, ForeignKey("ibron.ibron_cd"), comment="Informatiebron code")
    internet_domein: Mapped[str | None] = mapped_column(VARCHAR(200), comment="Internet domeinnaam")
    lidw_sgebr: Mapped[str | None] = mapped_column(VARCHAR(12), comment="Lidwoord van de organisatie")
    naam_officieel: Mapped[str] = mapped_column(VARCHAR(4000), comment="Taken van de organistorische eenheid")
    naam_spraakgbr: Mapped[str] = mapped_column(
        VARCHAR(255), comment="Naam die gebruikt voor in het 'normale' spraakgebruik"
    )
    plaats: Mapped[str | None] = mapped_column(VARCHAR(30), comment="(Woon)plaats")
    postcode: Mapped[str | None] = mapped_column(VARCHAR(7), comment="Nederlandse postcode")
    provincie: Mapped[str | None] = mapped_column(VARCHAR(30), comment="Provincie")
    straat: Mapped[str | None] = mapped_column(VARCHAR(30), comment="Straatnaam")
    telefoon: Mapped[str | None] = mapped_column(VARCHAR(30), comment="Telefoonnummer")

    # Relationships
    entity_ibron: Mapped["Ibron"] = relationship("Ibron", foreign_keys=[ibron_cd])  # type: ignore # noqa: F821
    parent_entities: Mapped[list["OeKoepelOe"]] = relationship(
        "OeKoepelOe",
        primaryjoin="Oe.oe_cd == OeKoepelOe.oe_cd",
        back_populates="child_entity",
    )

    @hybrid_property
    def count_parents(self) -> int:
        return len(self.parent_entities)


class OeKoepel(Base, DefaultColumns):
    """
    Table description: Overkoepelende organisatie
    """

    __tablename__ = "oe_koepel"
    __table_args__ = {"comment": "Overkoepelende organisatie"}

    oe_koepel_cd: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        comment="Koepel organisatie code",
    )
    titel: Mapped[str | None] = mapped_column(VARCHAR(255), comment="Titel van de koepelorganisatie")
    omschrijving: Mapped[str | None] = mapped_column(VARCHAR(4000), comment="Omschrijving van de koepelorganisatie")

    child_entities: Mapped[list["OeKoepelOe"]] = relationship(
        "OeKoepelOe",
        primaryjoin="OeKoepel.oe_koepel_cd == OeKoepelOe.oe_koepel_cd",
        back_populates="parent_entity",
    )

    @hybrid_property
    def count_children(self) -> int:
        return len(self.child_entities)


class OeKoepelOe(Base, DefaultColumns):
    """
    Table description: hiërarchische structuur van organisaties en koepelorganisaties
    """

    __tablename__ = "oe_koepel_oe"
    __table_args__ = {"comment": "Hiërarchische structuur van organisaties en koepelorganisaties"}

    oe_koepel_oe_cd: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Koppeling organisatie code")
    oe_cd: Mapped[int] = mapped_column(Integer, ForeignKey("oe.oe_cd"), comment="(child) organisatie code")
    oe_koepel_cd: Mapped[int] = mapped_column(
        Integer, ForeignKey("oe_koepel.oe_koepel_cd"), comment="Koepel organisatie code"
    )

    child_entity: Mapped["Oe"] = relationship("Oe", foreign_keys=[oe_cd], lazy="selectin")
    parent_entity: Mapped["OeKoepel"] = relationship("OeKoepel", foreign_keys=[oe_koepel_cd], lazy="selectin")


class OeComType(Base, DefaultColumns):
    """
    Table description: communicatie kanalen die gebruikt worden door organisaties
    """

    __tablename__ = "oe_com_type"
    __table_args__ = {"comment": "Communicatie kanalen die gebruikt worden door organisaties"}

    oe_com_type_cd: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Communicatiekanaal type code")
    omschrijving: Mapped[str] = mapped_column(VARCHAR(4000), comment="Omschrijving van het kanaal")

    # Relationships
    entities_oe_com_type: Mapped["EvtpOeComType"] = relationship(  # type: ignore # noqa: F821
        "EvtpOeComType",
        primaryjoin="OeComType.oe_com_type_cd == EvtpOeComType.oe_com_type_cd",
        back_populates="entity_oe_com_type",
        uselist=False,
    )
