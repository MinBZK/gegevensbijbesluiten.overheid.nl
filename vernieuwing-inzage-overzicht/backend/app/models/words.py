from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Words(Base):
    __tablename__ = "words"

    word: Mapped[str] = mapped_column(Text, primary_key=True)
