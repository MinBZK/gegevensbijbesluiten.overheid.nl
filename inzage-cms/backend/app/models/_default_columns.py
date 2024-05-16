from datetime import datetime

from sqlalchemy import VARCHAR, DateTime, func, text
from sqlalchemy.orm import Mapped, mapped_column


class DefaultColumns:
    notitie: Mapped[str | None] = mapped_column(VARCHAR(4000), comment="Notitieveld")
    user_nm: Mapped[str | None] = mapped_column(VARCHAR(30), comment="Gebruikersnaam", server_default="ICTU")
    ts_mut: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), comment="Tijdstip laatste mutatie"
    )
    ts_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("'2023-01-01 00:00:00+00'::timestamp with time zone"),
        comment="Tijdstip start datum",
    )
    ts_end: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("'9999-12-31 23:59:59.999999+00'::timestamp with time zone"),
        comment="Tijdstip einde datum",
    )
