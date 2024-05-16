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


class GstGg(Base):
    """
    Gegevensstroom Gegevensgroep
    TabelLabelLang: De koppeling tussen GST en GG
    Comment: Relatie tussen gegevensstroom, gegevensgroep
    """

    __tablename__ = "gst_gg"

    gst_gg_cd: Mapped[int] = mapped_column(Integer, primary_key=True)
    gg_cd: Mapped[int] = mapped_column(Integer, ForeignKey("gg.gg_cd"))
    gst_cd: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("evtp_gst.gst_cd"),
    )
    notitie: Mapped[str] = mapped_column(String)
    user_nm: Mapped[str] = mapped_column(String)
    ts_mut: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    sort_key: Mapped[int] = mapped_column(Integer)
    ts_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ts_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # Relationships
    entity_gg_child = relationship("Gg", foreign_keys=[gg_cd])
