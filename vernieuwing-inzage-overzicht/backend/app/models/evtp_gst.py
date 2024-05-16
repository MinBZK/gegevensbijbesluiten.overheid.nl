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


class EvtpGst(Base):
    """
    Besluit-gegevensstroom
    TabelLabelLang: De koppeling tussen besluiten en gegevensstromen
    Comment: Cross-reference tusen besluiten en gegevensstromen
    """

    __tablename__ = "evtp_gst"

    evtp_gst_cd: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    conditie: Mapped[str] = mapped_column(String)
    evtp_cd: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("evtp_version.evtp_cd"),
    )
    gst_cd: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("gst.gst_cd"),
    )
    notitie: Mapped[str] = mapped_column(String)
    sort_key: Mapped[int] = mapped_column(Integer)
    user_nm: Mapped[str] = mapped_column(String)
    ts_mut: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ts_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ts_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # Relationships
    entity_gst = relationship(
        "Gst",
        primaryjoin="EvtpGst.gst_cd == Gst.gst_cd",
        viewonly=True,
    )
    entities_gst_gg = relationship(
        "GstGg",
        primaryjoin="and_(EvtpGst.gst_cd == foreign(GstGg.gst_cd), EvtpGst.ts_start < foreign(GstGg.ts_end), EvtpGst.ts_end >= foreign(GstGg.ts_end))",
        uselist=True,
    )
    entities_gst_rge = relationship(
        "GstRge",
        primaryjoin="and_(EvtpGst.gst_cd == foreign(GstRge.gst_cd), EvtpGst.ts_start < foreign(GstRge.ts_end), EvtpGst.ts_end >= foreign(GstRge.ts_end))",
        uselist=True,
    )
    entity_evtp_version = relationship(
        "EvtpVersion",
        primaryjoin="and_(EvtpVersion.evtp_cd == EvtpGst.evtp_cd, EvtpVersion.id_publicatiestatus < 4, EvtpVersion.ts_start < EvtpGst.ts_end, EvtpVersion.ts_end > EvtpGst.ts_start)",
        back_populates="entities_evtp_gst",
    )
