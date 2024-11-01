from pydantic import HttpUrl
from sqlalchemy import VARCHAR, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base
from app.models._default_columns import DefaultColumns


class Rge(Base, DefaultColumns):
    """
    Table description: (onderdeel van) wet- en regelgeving - kunnen wetten zijn maar ook wetsartikelen of uitvoeringsregelingen
    """

    __tablename__ = "rge"
    __table_args__ = {
        "comment": "(Onderdeel van) wet- en regelgeving - kunnen wetten zijn maar ook wetsartikelen of uitvoeringsregelingen"
    }

    rge_cd: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Regelingelement code")
    re_link: Mapped[HttpUrl | None] = mapped_column(VARCHAR(300), comment="Link naar wet of regelgeving")
    tekst: Mapped[str | None] = mapped_column(VARCHAR(4000), comment="Officiele tekst")
    titel: Mapped[str] = mapped_column(
        VARCHAR(255),
        comment="Naam/omschrijving/titel van een regelingelement",
    )
