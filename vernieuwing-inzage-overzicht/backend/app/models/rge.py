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


class Rge(Base):
    """
    RegelingElement
    TabelLabelLang: Wet of regelgeving waarnaar verwezen wordt
    Comment: (Onderdeel van) wet- en regelgeving - kunnen wetten zijn maar ook wetsartikelen of uitvoeringsregelingen
    """

    __tablename__ = "rge"

    rge_cd: Mapped[int] = mapped_column(Integer, primary_key=True)
    notitie: Mapped[str] = mapped_column(String)
    re_link: Mapped[str] = mapped_column(String)
    tekst: Mapped[str] = mapped_column(String)
    titel: Mapped[str] = mapped_column(String)
    ts_mut: Mapped[str] = mapped_column(String)
    user_nm: Mapped[str] = mapped_column(String)
    ts_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ts_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))
