"""add_organisatie_omgeving

Revision ID: f0b292ced71a
Revises: 8c43eb7d0ccd
Create Date: 2024-08-13 10:13:14.995315

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f0b292ced71a"
down_revision = "8c43eb7d0ccd"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "omg",
        sa.Column("omg_cd", sa.Integer(), autoincrement=True, primary_key=True, comment="Omgeving code"),
        sa.Column("titel", sa.VARCHAR(255), nullable=False, comment="Naam van de omgeving"),
        sa.Column("oe_cd", sa.Integer(), nullable=False, comment="Gerelateerde organisatie code"),
        sa.Column("lidw", sa.VARCHAR(12), nullable=True, comment="Lidwoord"),
        sa.Column("link", sa.VARCHAR(2000), nullable=False, comment="Hyperlink naar de omgeving"),
        sa.Column(
            "notitie",
            sa.VARCHAR(2000),
            nullable=True,
            comment="Notitieveld",
        ),
        sa.Column(
            "user_nm",
            sa.VARCHAR(30),
            nullable=False,
            server_default="ICTU",
            comment="User identification",
        ),
        sa.Column(
            "ts_mut",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
            comment="Tijdstip laatste mutatie",
        ),
        sa.Column(
            "ts_start",
            sa.DateTime(timezone=True),
            server_default=sa.text("'2023-12-01'"),
            nullable=False,
            comment="Tijdstip aanmaakdatum",
        ),
        sa.Column(
            "ts_end",
            sa.DateTime(timezone=True),
            server_default=sa.text("'9999-12-31 23:59:59.999999+00'"),
            nullable=False,
            comment="Tijdstip einde datum",
        ),
        comment="Onderwerpen tabel",
    )

    op.add_column(
        "evtp_version",
        sa.Column(
            "omg_cd",
            sa.INTEGER(),
            sa.ForeignKey(
                "omg.omg_cd",
                name="fk_evtp_version_omg_cd_omg",
            ),
            autoincrement=False,
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_table("omg")
    op.drop_column("evtp_version", "omg_cd")
