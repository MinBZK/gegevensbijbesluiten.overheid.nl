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


class Gst(Base):
    """
    Gegevensstroom
    TabelLabelLang: Gegevensstroom die tussen organisatorische eenheden loopt
    Comment: Gegevensstroom die tussen organisatorische eenheden loopt
    """

    __tablename__ = "gst"

    gst_cd: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("evtp_gst.gst_cd"),
        primary_key=True,
    )
    gst_upc: Mapped[int] = mapped_column(Integer)
    omschrijving: Mapped[str] = mapped_column(String)
    oe_bron: Mapped[int] = mapped_column(Integer, ForeignKey("oe.oe_cd"))
    oe_best: Mapped[int] = mapped_column(Integer, ForeignKey("oe.oe_cd"))
    ibron_cd: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("ibron.ibron_cd"),
    )
    notitie: Mapped[str] = mapped_column(String)
    ext_lnk_aut: Mapped[str] = mapped_column(String)
    ts_mut: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    user_nm: Mapped[str] = mapped_column(String)
    ts_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ts_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # Relationships
    entity_oe_best = relationship(
        "Oe",
        foreign_keys=[oe_best],
    )
    entity_oe_bron = relationship(
        "Oe",
        foreign_keys=[oe_bron],
    )
    entity_ibron = relationship(
        "Ibron",
        foreign_keys=[ibron_cd],
    )
    entities_gst_gstt = relationship(
        "GstGstt",
        primaryjoin="and_(Gst.gst_cd == GstGstt.gst_cd, EvtpVersion.ts_start < GstGstt.ts_end, EvtpVersion.ts_end > GstGstt.ts_start)",
        uselist=True,
    )
