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


class GstRge(Base):
    """
    Gegevensstroom GegevensgroepRegeling Element
    TabelLabelLang: De koppeling tussen GST, GG en RGE
    Comment: Relatie tussen gegevensstroom, gegevensgroep en regelingelement inclusief sortering
    """

    __tablename__ = "gst_rge"

    gst_rge_cd: Mapped[int] = mapped_column(Integer, primary_key=True)
    gst_cd: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("evtp_gst.gst_cd"),
    )
    rge_cd: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("rge.rge_cd"),
    )
    notitie: Mapped[str] = mapped_column(String)
    user_nm: Mapped[str] = mapped_column(String)
    ts_mut: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    sort_key: Mapped[int] = mapped_column(Integer)
    ts_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ts_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # Relationships
    entity_rge = relationship(
        "Rge",
        primaryjoin="Rge.rge_cd == GstRge.rge_cd",
    )
