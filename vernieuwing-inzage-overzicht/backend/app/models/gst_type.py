from datetime import datetime

from sqlalchemy import (
    DateTime,
    Integer,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.database import Base


class GstType(Base):
    """
    GegevensstroomType
    TabelLabelLang: Gegevensstroom types
    Comment: Type gegevensstroom
    """

    __tablename__ = "gst_type"

    gstt_cd: Mapped[int] = mapped_column(Integer, primary_key=True)
    gstt_naam: Mapped[str] = mapped_column(String)
    gstt_oms: Mapped[str] = mapped_column(String)
    gstt_pp: Mapped[str] = mapped_column(String)
    ts_mut: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    user_nm: Mapped[str] = mapped_column(String)
    ts_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ts_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))
