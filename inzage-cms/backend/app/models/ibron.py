from sqlalchemy import VARCHAR, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.models._default_columns import DefaultColumns


class Ibron(Base, DefaultColumns):
    """
    Table description: register waar de gegevens afkomstig van zijn.
    """

    __tablename__ = "ibron"
    __table_args__ = {"comment": "register waar de gegevens afkomstig van zijn"}

    ibron_cd: Mapped[int] = mapped_column(Integer, primary_key=True, comment="Informatiebron code")
    oe_cd: Mapped[int | None] = mapped_column(Integer, ForeignKey("oe.oe_cd"), comment="Organisatie code")
    omschrijving: Mapped[str] = mapped_column(VARCHAR(80), comment="Omschrijving van de bron")

    entity_oe: Mapped["Oe"] = relationship(  # noqa: F821
        foreign_keys=[oe_cd],
    )
