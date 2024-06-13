"""add columns and delete deprecated columns

Revision ID: 41541fdd0c28
Revises: c90d8823bbf8
Create Date: 2023-10-05 13:15:32.457781

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "41541fdd0c28"
down_revision = "c90d8823bbf8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "evtp_oe_com_type",
        sa.Column(
            "ts_mut",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
            comment="Tijdstip laatste mutatie",
        ),
    )
    op.add_column(
        "evtp_oe_com_type",
        sa.Column(
            "user_nm",
            sa.VARCHAR(length=30),
            nullable=False,
            server_default=sa.text("'PVZ'"),
            comment="User identification",
        ),
    )
    op.add_column(
        "gst_gstt",
        sa.Column(
            "user_nm",
            sa.VARCHAR(length=30),
            nullable=False,
            server_default=sa.text("'PVZ'"),
            comment="User identification",
        ),
    )
    op.add_column(
        "gst_gstt",
        sa.Column(
            "ts_mut",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
            comment="Tijdstip laatste mutatie",
        ),
    )
    op.add_column(
        "evtp_gst",
        sa.Column(
            "user_nm",
            sa.VARCHAR(length=30),
            nullable=False,
            server_default=sa.text("'PVZ'"),
            comment="User identification",
        ),
    )
    op.add_column(
        "gst_gg_rge",
        sa.Column(
            "user_nm",
            sa.VARCHAR(length=30),
            nullable=False,
            server_default=sa.text("'PVZ'"),
            comment="User identification",
        ),
    )
    op.add_column(
        "evtp_version",
        sa.Column(
            "ts_publ",
            sa.TIMESTAMP(timezone=True),
            nullable=True,
            comment="Tijdstip publicatie",
        ),
    )

    op.execute("UPDATE evtp_version SET ts_publ = CURRENT_TIMESTAMP")

    op.alter_column("evtp", "evtp_upc", nullable=False)
    op.alter_column("evtp_acc", "evtp_cd", nullable=False)
    op.alter_column("evtp_acc", "oe_cd", nullable=False)
    op.alter_column("evtp_acc", "bestand_acc_cd", nullable=False)
    op.alter_column("evtp_gst", "gst_cd", nullable=False)
    op.alter_column("evtp_gst", "evtp_cd", nullable=False)
    op.alter_column("evtp_version", "huidige_versie", nullable=False)
    op.alter_column("gg_struct", "gg_cd_sub", nullable=False)
    op.alter_column("gg_struct", "gg_cd_sup", nullable=False)
    op.alter_column("gst", "oe_bron", nullable=False)
    op.alter_column("gst", "oe_best", nullable=False)
    op.alter_column("gst", "gst_upc", nullable=False)
    op.alter_column("gst_gg_rge", "gst_cd", nullable=False)
    op.alter_column("gst_gg_rge", "gg_cd", nullable=False)
    op.alter_column("gst_gg_rge", "rge_cd", nullable=False)
    op.alter_column("gst_gstt", "gst_cd", nullable=False)
    op.alter_column("gst_gstt", "gstt_cd", nullable=False)
    op.alter_column("oe", "oe_type_cd", nullable=False)
    op.alter_column("oe_struct", "oe_cd_sub", nullable=False)
    op.alter_column("oe_struct", "oe_cd_sup", nullable=False)
    op.alter_column("oe_struct", "osrt_cd", nullable=False)

    op.drop_column("rge", "re_type")
    op.drop_column("gg", "ibron_cd")


def downgrade() -> None:
    op.drop_column("gst_gstt", "ts_mut")
    op.drop_column("gst_gstt", "user_nm")
    op.drop_column("evtp_oe_com_type", "ts_mut")
    op.drop_column("evtp_oe_com_type", "user_nm")
    op.drop_column("evtp_gst", "user_nm")
    op.drop_column("gst_gg_rge", "user_nm")

    op.alter_column("oe_struct", "osrt_cd", nullable=True)
    op.alter_column("oe_struct", "oe_cd_sup", nullable=True)
    op.alter_column("oe_struct", "oe_cd_sub", nullable=True)
    op.alter_column("oe", "oe_type_cd", nullable=True)
    op.alter_column("gst_gstt", "gstt_cd", nullable=True)
    op.alter_column("gst_gstt", "gst_cd", nullable=True)
    op.alter_column("gst_gg_rge", "rge_cd", nullable=True)
    op.alter_column("gst_gg_rge", "gg_cd", nullable=True)
    op.alter_column("gst_gg_rge", "gst_cd", nullable=True)
    op.alter_column("gst", "gst_upc", nullable=True)
    op.alter_column("gst", "oe_best", nullable=True)
    op.alter_column("gst", "oe_bron", nullable=True)
    op.alter_column("gg_struct", "gg_cd_sup", nullable=True)
    op.alter_column("gg_struct", "gg_cd_sub", nullable=True)
    op.alter_column("evtp_version", "huidige_versie", nullable=True)
    op.alter_column("evtp_version", "oe_best", nullable=True)
    op.alter_column("evtp_gst", "evtp_cd", nullable=True)
    op.alter_column("evtp_gst", "gst_cd", nullable=True)
    op.alter_column("evtp_acc", "bestand_acc_cd", nullable=True)
    op.alter_column("evtp_acc", "oe_cd", nullable=True)
    op.alter_column("evtp_acc", "evtp_cd", nullable=True)
    op.alter_column("evtp", "evtp_upc", nullable=True)

    op.add_column(
        "gg",
        sa.Column("ibron_cd", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "rge",
        sa.Column("re_type", sa.String(length=255), nullable=True),
    )
