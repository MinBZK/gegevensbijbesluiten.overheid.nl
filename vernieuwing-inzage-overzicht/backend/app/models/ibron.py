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


class Ibron(Base):
    """
    Informatiebron
    TabelLabelLang: Registraties waar organisatorische eenheden gegevens vastleggen
    Comment: Registratie waar de gegevens afkomstig van zijn.
    """

    __tablename__ = "ibron"

    ibron_cd: Mapped[int] = mapped_column(Integer, primary_key=True)
    oe_cd: Mapped[int] = mapped_column(Integer, ForeignKey("oe.oe_cd"))
    omschrijving: Mapped[str] = mapped_column(String)
    notitie: Mapped[str] = mapped_column(String)
    ts_mut: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    user_nm: Mapped[str] = mapped_column(String)
    ts_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ts_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # Relationships
    entity_oe = relationship(
        "Oe",
        foreign_keys=[oe_cd],
    )
