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


class EvtpOeComType(Base):
    """
    EvtpOeComType
    TabelLabelLang: De koppeling tussen besluiten en organisatie communicatie kanalen
    Comment: Cross-reference tusen evtp en oe_com_type
    """

    __tablename__ = "evtp_oe_com_type"

    evtp_oe_com_type_cd: Mapped[int] = mapped_column(Integer, primary_key=True)
    evtp_cd: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("evtp_version.evtp_cd"),
    )
    oe_com_type_cd: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("oe_com_type.oe_com_type_cd"),
    )
    link: Mapped[str] = mapped_column(String)
    user_nm: Mapped[str] = mapped_column(String)
    ts_mut: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ts_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ts_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # Relationships
    entity_oe_com_type = relationship(
        "OeComType",
        foreign_keys=[oe_com_type_cd],
    )
