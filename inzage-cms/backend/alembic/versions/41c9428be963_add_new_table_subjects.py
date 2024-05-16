"""add new table subjects

Revision ID: 41c9428be963
Revises: 41541fdd0c28
Create Date: 2023-12-06 17:57:17.279586

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "41c9428be963"
down_revision = "41541fdd0c28"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ond",
        sa.Column("ond_cd", sa.Integer(), autoincrement=True, primary_key=True, comment="Onderwerp code"),
        sa.Column("titel", sa.VARCHAR(255), nullable=False, comment="Titel van het onderwerp"),
        sa.Column("omschrijving", sa.VARCHAR(4000), nullable=False, comment="Omschrijving van het onderwerp"),
        sa.Column("sort_key", sa.Integer(), nullable=False, comment="Sorteer volgorde van het onderwerp"),
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

    op.create_table(
        "evtp_ond",
        sa.Column(
            "evtp_ond_cd",
            sa.Integer(),
            autoincrement=True,
            primary_key=True,
            comment="Onderwerpen besluiten code",
        ),
        sa.Column(
            "ond_cd",
            sa.Integer(),
            sa.ForeignKey("ond.ond_cd", name="evptond_ond_fk"),
            nullable=False,
            comment="Onderwerp code",
        ),
        sa.Column(
            "evtp_cd",
            sa.Integer(),
            sa.ForeignKey("evtp.evtp_cd", name="evptond_evtp_fk"),
            nullable=False,
            comment="Event type code",
        ),
        sa.Column("user_nm", sa.VARCHAR(30), nullable=False, comment="User identification"),
        sa.Column("notitie", sa.VARCHAR(2000), nullable=True, comment="Notitieveld"),
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
        comment="Relatie tussen onderwerpen en besluiten",
    )

    op.drop_column("gst_gg_rge", "ibron_cd")

    with open("app/database/setup/2.set_up_ond.sql") as file:
        op.execute(file.read())


def downgrade() -> None:
    op.drop_table("evtp_ond")
    op.drop_table("ond")
    op.add_column(
        "gst_gg_rge",
        sa.Column("ibron_cd", sa.Integer(), sa.ForeignKey("ibron.ibron_cd", name="ggr_ibron_fk"), nullable=True),
    )
