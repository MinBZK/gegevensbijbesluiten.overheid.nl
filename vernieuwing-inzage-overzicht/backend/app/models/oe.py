from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.database import Base


class OeStruct(Base):
    """
    OrganisatieStructuur
    TabelLabelLang: Hiërarchie van organisatorische eenheden
    Comment: Relatie van een bepaald type tussen twee organisatorische eenheden/instanties
    """

    __tablename__ = "oe_struct"

    oe_struct_cd: Mapped[int] = mapped_column(Integer, primary_key=True)
    oe_cd_sub: Mapped[int] = mapped_column(Integer, ForeignKey("oe.oe_cd"))
    oe_cd_sup: Mapped[int] = mapped_column(Integer, ForeignKey("oe.oe_cd"))
    notitie: Mapped[str] = mapped_column(String)
    ts_mut: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    user_nm: Mapped[str] = mapped_column(String)
    ts_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ts_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    child_entity = relationship(
        "Oe",
        foreign_keys=[oe_cd_sub],
    )
    parent_oe_entity = relationship(
        "Oe",
        foreign_keys=[oe_cd_sup],
    )


class Oe(Base):
    """
    Organisatie
    TabelLabelLang: De organisaties die gegevens uitwisselen t.b.v. een gegevensstroom
    Comment: Organisatorische eenheid/instantie of soort van organisatorische entiteit
    """

    __tablename__ = "oe"

    oe_cd: Mapped[int] = mapped_column(Integer, primary_key=True)
    oe_upc: Mapped[int] = mapped_column(Integer, primary_key=True)
    afko: Mapped[str] = mapped_column(String)
    e_contact: Mapped[str] = mapped_column(String)
    huisnummer: Mapped[str] = mapped_column(String)
    huisnummer_toev: Mapped[str] = mapped_column(String)
    ibron_cd: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("ibron.ibron_cd"),
    )
    internet_domein: Mapped[str] = mapped_column(String)
    lidw_sgebr: Mapped[str] = mapped_column(String)
    naam_officieel: Mapped[str] = mapped_column(String)
    naam_spraakgbr: Mapped[str] = mapped_column(String)
    notitie: Mapped[str] = mapped_column(String)
    plaats: Mapped[str] = mapped_column(String)
    postcode: Mapped[str] = mapped_column(String)
    provincie: Mapped[str] = mapped_column(String)
    straat: Mapped[str] = mapped_column(String)
    telefoon: Mapped[str] = mapped_column(String)
    ts_mut: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    user_nm: Mapped[str] = mapped_column(String)
    ts_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ts_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # Relationships
    entity_ibron = relationship("Ibron", foreign_keys=[ibron_cd])

    parent_oe_struct = relationship(
        "OeStruct",
        primaryjoin="Oe.oe_cd == OeStruct.oe_cd_sub",
    )

    child_oe_struct = relationship(
        "OeStruct",
        primaryjoin="Oe.oe_cd == OeStruct.oe_cd_sup",
    )

    parent_oe_entity = relationship(
        "Oe",
        secondary=OeStruct.__table__,
        primaryjoin="Oe.oe_cd == OeStruct.oe_cd_sub",
        secondaryjoin="Oe.oe_cd == OeStruct.oe_cd_sup",
        back_populates="child_oe_entity",
    )

    child_oe_entity = relationship(
        "Oe",
        secondary=OeStruct.__table__,
        primaryjoin="Oe.oe_cd == OeStruct.oe_cd_sup",
        secondaryjoin="Oe.oe_cd == OeStruct.oe_cd_sub",
        back_populates="parent_oe_entity",
        # viewonly=True
    )
