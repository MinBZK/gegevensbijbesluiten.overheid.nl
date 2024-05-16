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


class GstGstt(Base):
    """
    Gegevensstroom GegevensstroomType
    TabelLabelLang: De koppeling tussen gegevensstroom en gegevensstroomType
    Comment: Relatie tussen gegevensstroom en gegevensstroomtype
    """

    __tablename__ = "gst_gstt"
    gst_gstt_cd: Mapped[int] = mapped_column(Integer, primary_key=True)
    gstt_cd: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("gst_type.gstt_cd"),
    )
    gst_cd: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("gst.gst_cd"),
    )
    user_nm: Mapped[str] = mapped_column(String)
    ts_mut: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ts_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ts_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # Relationships
    entity_gst_type = relationship(
        "GstType",
        primaryjoin="GstGstt.gstt_cd == GstType.gstt_cd",
    )
