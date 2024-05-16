from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.ext.hybrid import (
    hybrid_property,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.database import Base


class GgStruct(Base):
    """
    GegevensgroepStructuur
    TabelLabelLang: Hiërarchie van gegevens(groepen)
    Comment: Relatie tussen gegevensgroepen van een bepaalde soort
    """

    __tablename__ = "gg_struct"

    gg_struct_cd: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    gg_cd_sub: Mapped[int] = mapped_column(Integer, ForeignKey("gg.gg_cd"))
    gg_cd_sup: Mapped[int] = mapped_column(Integer, ForeignKey("gg.gg_cd"))
    notitie: Mapped[str] = mapped_column(String)
    ts_mut: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    user_nm: Mapped[str] = mapped_column(String)
    ts_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ts_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # Relationships
    child_entity = relationship(
        "Gg",
        foreign_keys=[gg_cd_sub],
    )
    parent_gg_entity = relationship(
        "Gg",
        foreign_keys=[gg_cd_sup],
    )


class Gg(Base):
    """
    Gegevensgroep
    TabelLabelLang: Gegevensgroep die in een gegevensstroom voorkomt
    Comment: Gegevensgroepen die in gegevensstromen worden gebruikt om uit te wisselen
    """

    __tablename__ = "gg"

    gg_cd: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("gg_struct.gg_cd_sub"),
        primary_key=True,
        index=True,
    )
    gg_upc: Mapped[int] = mapped_column(Integer)
    omschrijving: Mapped[str] = mapped_column(String)
    omschrijving_uitgebreid: Mapped[str] = mapped_column(String)
    user_nm: Mapped[str] = mapped_column(String)
    ts_mut: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    notitie: Mapped[str] = mapped_column(String)
    sort_key: Mapped[int] = mapped_column(Integer)
    ts_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ts_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    parent_gg_struct = relationship(
        "GgStruct",
        primaryjoin="Gg.gg_cd == GgStruct.gg_cd_sub",
    )

    child_gg_struct = relationship(
        "GgStruct",
        primaryjoin="Gg.gg_cd == GgStruct.gg_cd_sup",
    )

    gst_gg_entity = relationship(
        "GstGg",
        primaryjoin="Gg.gg_cd == GstGg.gg_cd",
    )

    parent_gg_entity = relationship(
        "Gg",
        secondary=GgStruct.__table__,
        primaryjoin="Gg.gg_cd == GgStruct.gg_cd_sub",
        secondaryjoin="Gg.gg_cd == GgStruct.gg_cd_sup",
        back_populates="child_gg_entity",
    )

    child_gg_entity = relationship(
        "Gg",
        secondary=GgStruct.__table__,
        primaryjoin="Gg.gg_cd == GgStruct.gg_cd_sup",
        secondaryjoin="Gg.gg_cd == GgStruct.gg_cd_sub",
        back_populates="parent_gg_entity",
        # viewonly=True
    )

    evtp_sort = relationship(
        "GgEvtpSort",
        primaryjoin="Gg.gg_cd == GgEvtpSort.gg_cd",
        viewonly=True,
    )

    @hybrid_property
    def evtp_sort_key(
        self,
    ) -> dict[int, int]:
        """Create a dict with all sort_keys per evtp"""
        if not any(self.evtp_sort):
            return {}
        return {item.evtp_cd: item.sort_key for item in self.evtp_sort}


class GgEvtpSort(Base):
    """
    Table description: sorteertabel om individueel de sorteersleutel van een (koepel)gegevensgroep te overrulen per besluit
    """

    __tablename__ = "gg_evtp_sort"
    __table_args__ = {"comment": "sort_key gg op basis van evtp"}
    gg_evtp_sort_cd: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        comment="Koepelgegevensgroep-Besluit sortering code",
    )
    gg_cd: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("gg.gg_cd"),
        comment="Koepelgegevensgroep code",
    )
    evtp_cd: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("evtp.evtp_cd"),
        comment="Besluit code",
    )

    sort_key: Mapped[int] = mapped_column(
        Integer,
        comment="Sorteer volgorde van de koepelgegevensgroep in een besluit",
    )
    gg = relationship(
        "Gg",
        foreign_keys=[gg_cd],
    )
