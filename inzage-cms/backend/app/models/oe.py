from sqlalchemy import VARCHAR, Boolean, ForeignKey, Integer
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
    parent_entities: Mapped[list["OeStruct"]] = relationship(
        "OeStruct",
        primaryjoin="Oe.oe_cd == OeStruct.oe_cd_sub",
        back_populates="child_entity",
    )
    child_entities: Mapped[list["OeStruct"]] = relationship(
        "OeStruct",
        primaryjoin="Oe.oe_cd == OeStruct.oe_cd_sup",
        back_populates="parent_entity",
    )

    @hybrid_property
    def count_parents(self) -> int:
        return len(self.parent_entities)

    @hybrid_property
    def count_children(self) -> int:
        return len(self.child_entities)


class OeStruct(Base, DefaultColumns):
    """
    Table description: hiërarchische structuur van organisaties wat resulteert in een sub(=child)-sup(=parent) relatie
    """

    __tablename__ = "oe_struct"
    __table_args__ = {
        "comment": "Hiërarchische structuur van organisaties wat resulteert in een sub(=child)-sup(=parent) relatie"
    }

    oe_struct_cd: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Organisatie structuur code")
    oe_cd_sub: Mapped[int] = mapped_column(Integer, ForeignKey("oe.oe_cd"), comment="Sub (child) organisatie code")
    oe_cd_sup: Mapped[int] = mapped_column(Integer, ForeignKey("oe.oe_cd"), comment="Sup (parent) organisatie code")
    koepel: Mapped[bool | None] = mapped_column(Boolean, comment="Wel of geen koepel")

    # Relationships
    parent_entity: Mapped["Oe"] = relationship(
        "Oe",
        foreign_keys=[oe_cd_sup],
        back_populates="child_entities",
    )
    child_entity: Mapped["Oe"] = relationship("Oe", foreign_keys=[oe_cd_sub], back_populates="parent_entities")


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
