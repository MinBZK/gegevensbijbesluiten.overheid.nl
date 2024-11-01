from pydantic import HttpUrl
from sqlalchemy import VARCHAR, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.models._default_columns import DefaultColumns


class Ibron(Base, DefaultColumns):
    """
    Table description: registers, administraties, systemen etc. waarin gegevens worden beheerd door een organisatie.
    """

    __tablename__ = "ibron"
    __table_args__ = {
        "comment": "registers, administraties, systemen etc. waarin gegevens worden beheerd door een organisatie"
    }

    ibron_cd: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Informatiebron code")
    titel: Mapped[str] = mapped_column(VARCHAR(200), comment="Titel van de informatiebron")
    afko: Mapped[int | None] = mapped_column(VARCHAR(15), comment="Afkorting van de informatiebron")
    lidw: Mapped[int | None] = mapped_column(VARCHAR(12), comment="Lidwoord code van de bron")
    link: Mapped[HttpUrl | None] = mapped_column(VARCHAR(200), comment="Link naar de informatiebron")
    oe_cd: Mapped[int] = mapped_column(
        Integer, ForeignKey("oe.oe_cd"), comment="Organisatie die de informatiebron beheert"
    )

    entity_oe: Mapped["Oe"] = relationship(  # type: ignore # noqa: F821
        foreign_keys=[oe_cd],
    )
