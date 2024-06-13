from sqlalchemy import VARCHAR, Boolean, ForeignKey, Integer
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.models._default_columns import DefaultColumns


class Gg(Base, DefaultColumns):
    """
    Table description: groepen of elementaire soorten gegevens
    """

    __tablename__ = "gg"
    __table_args__ = {"comment": "Groepen of elementaire soorten gegevens"}

    gg_cd: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Gegevensgroep code")
    gg_upc: Mapped[int] = mapped_column(
        Integer, index=True, comment="Uniforme product code dat hoort bij een gegevensgroep"
    )
    omschrijving: Mapped[str] = mapped_column(VARCHAR(4000), comment="Naam van de gegevensgroep")
    omschrijving_uitgebreid: Mapped[str] = mapped_column(
        VARCHAR(4000), comment="Uitgebreide omschrijving van de gegevensgroep"
    )
    sort_key: Mapped[int | None] = mapped_column(
        Integer, comment="Sorteer volgorde van de koepelgegevensgroep in een besluit"
    )
    koepel: Mapped[bool | None] = mapped_column(Boolean, comment="Wel of geen koepel")

    # Relationships
    parent_entities: Mapped[list["GgStruct"]] = relationship(
        "GgStruct",
        primaryjoin="Gg.gg_cd == GgStruct.gg_cd_sub",
        back_populates="child_entity",
    )
    child_entities: Mapped[list["GgStruct"]] = relationship(
        "GgStruct",
        primaryjoin="Gg.gg_cd == GgStruct.gg_cd_sup",
        viewonly=True,
    )
    evtp_sort = relationship("GgEvtpSort", primaryjoin="Gg.gg_cd == GgEvtpSort.gg_cd", viewonly=True)

    @hybrid_property
    def count_parents(self) -> int:
        return len(self.parent_entities)

    @hybrid_property
    def count_children(self) -> int:
        return len(self.child_entities)


class GgStruct(Base, DefaultColumns):
    """
    Table description: hiërarchische structuur van gegevensgroepen wat resulteert in een sub(=child)-sup(=parent) relatie
    """

    __tablename__ = "gg_struct"
    __table_args__ = {
        "comment": "Hiërarchische structuur van gegevensgroepen wat resulteert in een sub(=child)-sup(=parent) relatie"
    }

    gg_struct_cd: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Gegevensgroepen structuur code")
    gg_cd_sub: Mapped[int] = mapped_column(Integer, ForeignKey("gg.gg_cd"), comment="Sub (child) gegevensgroep code")
    gg_cd_sup: Mapped[int] = mapped_column(Integer, ForeignKey("gg.gg_cd"), comment="Super (parent) gegevensgroep code")

    # Relationships
    parent_entity: Mapped["Gg"] = relationship(
        "Gg",
        foreign_keys=[gg_cd_sup],
        back_populates="child_entities",
    )
    child_entity: Mapped["Gg"] = relationship(
        "Gg",
        foreign_keys=[gg_cd_sub],
        back_populates="parent_entities",
    )


class GgEvtpSort(Base, DefaultColumns):
    """
    Table description: sorteertabel om individueel de sorteersleutel van een (koepel)gegevensgroep te overrulen per besluit
    """

    __tablename__ = "gg_evtp_sort"
    __table_args__ = {
        "comment": "Sorteertabel om individueel de sorteersleutel van een (koepel)gegevensgroep te overrulen per besluit"
    }

    gg_evtp_sort_cd: Mapped[int] = mapped_column(
        Integer, primary_key=True, comment="Koepelgegevensgroep-Besluit sortering code"
    )
    gg_cd: Mapped[int] = mapped_column(Integer, ForeignKey("gg.gg_cd"), comment="Koepelgegevensgroep code")
    evtp_cd: Mapped[int] = mapped_column(Integer, ForeignKey("evtp_version.evtp_cd"), comment="Besluit code")
    sort_key: Mapped[int] = mapped_column(Integer, comment="Sorteer volgorde van de koepelgegevensgroep in een besluit")

    # Relationships
    entity_gg: Mapped["Oe"] = relationship("Gg", foreign_keys=[gg_cd], viewonly=True)  # type: ignore # noqa: F821
    entity_evtp_version: Mapped["EvtpVersion"] = relationship(  # type: ignore # noqa: F821
        "EvtpVersion",
        foreign_keys=[evtp_cd],
    )
