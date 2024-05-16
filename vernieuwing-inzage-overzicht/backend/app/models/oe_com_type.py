from datetime import datetime

from sqlalchemy import (
    DateTime,
    Integer,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.database import Base


class OeComType(Base):
    """
    Organisatie Communicatie Type
    TabelLabelLang: Kanaal die een organisatie gebruikt om te communiceren
    Comment: Communicatie kanalen die gebruikt worden door organisaties
    """

    __tablename__ = "oe_com_type"

    oe_com_type_cd: Mapped[int] = mapped_column(Integer, primary_key=True)
    omschrijving: Mapped[str] = mapped_column(String)
    notitie: Mapped[str] = mapped_column(String)
    ts_mut: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    user_nm: Mapped[str] = mapped_column(String)
    ts_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ts_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # Relationships
    entities_oe_com_type = relationship(
        "EvtpOeComType",
        primaryjoin="and_(OeComType.oe_com_type_cd == EvtpOeComType.oe_com_type_cd)",
        back_populates="entity_oe_com_type",
    )
