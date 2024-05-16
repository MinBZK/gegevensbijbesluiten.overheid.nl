"""align sqlalchemy with db

Revision ID: 7a032cd9759b
Revises: 41c9428be963
Create Date: 2024-01-02 14:42:25.252379

"""

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "7a032cd9759b"
down_revision = "41c9428be963"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Make user_nm column uniform
    op.alter_column(
        "evtp_gst",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default="ICTU",
        existing_comment="User identification",
        existing_nullable=False,
    )
    op.alter_column(
        "evtp_oe_com_type",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default="ICTU",
        existing_comment="User identification",
        existing_nullable=False,
    )
    op.alter_column(
        "evtp_ond",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default="ICTU",
        existing_comment="User identification",
        existing_nullable=False,
    )
    op.alter_column(
        "evtp_version",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default="ICTU",
        comment="User identification",
        existing_nullable=False,
    )
    op.alter_column(
        "gg",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default="ICTU",
        comment="User identification",
        existing_comment="User identification.",
        existing_nullable=False,
    )
    op.alter_column(
        "gg_struct",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default="ICTU",
        comment="User identification",
        existing_comment="User identification.",
        existing_nullable=False,
    )
    op.alter_column(
        "gst",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default="ICTU",
        comment="User identification",
        existing_comment="User identification.",
        existing_nullable=False,
    )
    op.alter_column(
        "gst_gg_rge",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default="ICTU",
        existing_comment="User identification",
        existing_nullable=False,
    )
    op.alter_column(
        "gst_gstt",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default="ICTU",
        existing_comment="User identification",
        existing_nullable=False,
    )
    op.alter_column(
        "gst_type",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default="ICTU",
        comment="User identification",
        existing_comment="Id gebruiker",
        existing_nullable=False,
    )
    op.alter_column(
        "ibron",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default="ICTU",
        comment="User identification",
        existing_comment="User identification.",
        existing_nullable=False,
    )
    op.alter_column(
        "oe",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default="ICTU",
        comment="User identification",
        existing_comment="User identification.",
        existing_nullable=False,
    )
    op.alter_column(
        "oe_com_type",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default="ICTU",
        existing_comment="User identification",
        existing_nullable=False,
    )
    op.alter_column(
        "oe_struct",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default="ICTU",
        comment="User identification",
        existing_comment="User identification.",
        existing_nullable=False,
    )
    op.alter_column(
        "oe_type",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default="ICTU",
        comment="User identification",
        existing_comment="User identification.",
        existing_nullable=False,
    )
    op.alter_column(
        "oe_struct_rolt",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default="ICTU",
        comment="User identification",
        existing_comment="User identification.",
        existing_nullable=False,
    )
    op.alter_column(
        "ond",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default="ICTU",
        existing_comment="User identification",
        existing_nullable=False,
    )
    op.alter_column(
        "rge",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default="ICTU",
        comment="User identification",
        existing_comment="User identification.",
        existing_nullable=False,
    )

    # Make ts_mut column uniform
    op.alter_column(
        "evtp_gst",
        "ts_mut",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text("now()"),
        existing_comment="Tijdstip laatste mutatie",
        existing_nullable=False,
    )
    op.alter_column(
        "gg",
        "ts_mut",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text("now()"),
        existing_comment="Tijdstip laatste mutatie",
        existing_nullable=False,
    )
    op.alter_column(
        "gg_struct",
        "ts_mut",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text("now()"),
        existing_comment="Tijdstip laatste mutatie",
        existing_nullable=False,
    )
    op.alter_column(
        "gst",
        "ts_mut",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text("now()"),
        existing_comment="Tijdstip laatste mutatie",
        existing_nullable=False,
    )
    op.alter_column(
        "gst_gg_rge",
        "ts_mut",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text("now()"),
        existing_comment="Tijdstip laatste mutatie",
        existing_nullable=False,
    )
    op.alter_column(
        "gst_type",
        "ts_mut",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text("now()"),
        existing_comment="Tijdstip laatste mutatie",
        existing_nullable=False,
    )
    op.alter_column(
        "ibron",
        "ts_mut",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text("now()"),
        existing_comment="Tijdstip laatste mutatie",
        existing_nullable=False,
    )
    op.alter_column(
        "oe",
        "ts_mut",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text("now()"),
        existing_comment="Tijdstip laatste mutatie",
        existing_nullable=False,
    )
    op.alter_column(
        "oe_com_type",
        "ts_mut",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text("now()"),
        existing_comment="Tijdstip laatste mutatie",
        existing_nullable=False,
    )
    op.alter_column(
        "oe_struct",
        "ts_mut",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text("now()"),
        existing_comment="Tijdstip laatste mutatie",
        existing_nullable=False,
    )
    op.alter_column(
        "oe_type",
        "ts_mut",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text("now()"),
        existing_comment="Tijdstip laatste mutatie",
        existing_nullable=False,
    )
    op.alter_column(
        "oe_struct_rolt",
        "ts_mut",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text("now()"),
        existing_comment="Tijdstip laatste mutatie",
        existing_nullable=False,
    )

    op.create_index(op.f("ix_rubriekenvoorbeheer_tabelnaam"), "rubriekenvoorbeheer", ["tabelnaam"], unique=False)
    op.create_index(op.f("ix_tabellenvoorbeheer_tabelnaam"), "tabellenvoorbeheer", ["tabelnaam"], unique=False)

    # Add missing foreign keys
    op.create_foreign_key(
        op.f("fk_evtp_version_evtp_cd_evtp"), "evtp_version", "evtp", ["evtp_cd"], ["evtp_cd"], ondelete="cascade"
    )
    op.create_foreign_key(op.f("fk_ibron_oe_cd_oe"), "ibron", "oe", ["oe_cd"], ["oe_cd"])


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_tabellenvoorbeheer_tabelnaam"), table_name="tabellenvoorbeheer")
    op.create_index("idx_16555_tabelnaam_unique", "tabellenvoorbeheer", ["tabelnaam"], unique=False)
    op.drop_index(op.f("ix_rubriekenvoorbeheer_tabelnaam"), table_name="rubriekenvoorbeheer")
    op.create_index("idx_16546_rubriektabel_fk_idx", "rubriekenvoorbeheer", ["tabelnaam"], unique=False)
    op.create_index("idx_16536_reg_usr_fk", "rge", ["user_nm"], unique=False)
    op.alter_column(
        "rge",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default=None,
        comment="User identification.",
        existing_comment="User identification",
        existing_nullable=False,
    )
    op.alter_column(
        "ond",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default=None,
        existing_comment="User identification",
        existing_nullable=False,
    )
    op.create_index("idx_16517_oet_usr_fk", "oe_type", ["user_nm"], unique=False)
    op.alter_column(
        "oe_type",
        "ts_mut",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=None,
        existing_comment="Tijdstip laatste mutatie",
        existing_nullable=False,
    )
    op.alter_column(
        "oe_type",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default=None,
        comment="User identification.",
        existing_comment="User identification",
        existing_nullable=False,
    )
    op.create_index("idx_16512_osrt_usr_fk", "oe_struct_rolt", ["user_nm"], unique=False)
    op.alter_column(
        "oe_struct_rolt",
        "ts_mut",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=None,
        existing_comment="Tijdstip laatste mutatie",
        existing_nullable=False,
    )
    op.alter_column(
        "oe_struct_rolt",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default=None,
        comment="User identification.",
        existing_comment="User identification",
        existing_nullable=False,
    )
    op.create_index("idx_16507_oes_usr_fk", "oe_struct", ["user_nm"], unique=False)
    op.alter_column(
        "oe_struct",
        "ts_mut",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=None,
        existing_comment="Tijdstip laatste mutatie",
        existing_nullable=False,
    )
    op.alter_column(
        "oe_struct",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default=None,
        comment="User identification.",
        existing_comment="User identification",
        existing_nullable=False,
    )
    op.alter_column(
        "oe_com_type",
        "ts_mut",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=None,
        existing_comment="Tijdstip laatste mutatie",
        existing_nullable=False,
    )
    op.alter_column(
        "oe_com_type",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default=None,
        existing_comment="User identification",
        existing_nullable=False,
    )
    op.create_index("idx_16522_oe_usr_fk", "oe", ["user_nm"], unique=False)
    op.alter_column(
        "oe",
        "ts_mut",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=None,
        existing_comment="Tijdstip laatste mutatie",
        existing_nullable=False,
    )
    op.alter_column(
        "oe",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default=None,
        comment="User identification.",
        existing_comment="User identification",
        existing_nullable=False,
    )
    op.drop_constraint(op.f("fk_ibron_oe_cd_oe"), "ibron", type_="foreignkey")
    op.create_index("idx_16467_ibrn_usr_fk", "ibron", ["user_nm"], unique=False)
    op.alter_column(
        "ibron",
        "ts_mut",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=None,
        existing_comment="Tijdstip laatste mutatie",
        existing_nullable=False,
    )
    op.alter_column(
        "ibron",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default=None,
        comment="User identification.",
        existing_comment="User identification",
        existing_nullable=False,
    )
    op.alter_column(
        "gst_type",
        "ts_mut",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=None,
        existing_comment="Tijdstip laatste mutatie",
        existing_nullable=False,
    )
    op.alter_column(
        "gst_type",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default=None,
        comment="Id gebruiker",
        existing_comment="User identification",
        existing_nullable=False,
    )
    op.alter_column(
        "gst_gstt",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default=sa.text("'PVZ'::character varying"),
        existing_comment="User identification",
        existing_nullable=False,
    )
    op.alter_column(
        "gst_gg_rge",
        "ts_mut",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=None,
        existing_comment="Tijdstip laatste mutatie",
        existing_nullable=False,
    )
    op.alter_column(
        "gst_gg_rge",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default=sa.text("'PVZ'::character varying"),
        existing_comment="User identification",
        existing_nullable=False,
    )
    op.create_index("idx_16420_gst_usr_fk", "gst", ["user_nm"], unique=False)
    op.alter_column(
        "gst",
        "ts_mut",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=None,
        existing_comment="Tijdstip laatste mutatie",
        existing_nullable=False,
    )
    op.alter_column(
        "gst",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default=None,
        comment="User identification.",
        existing_comment="User identification",
        existing_nullable=False,
    )
    op.create_index("idx_16429_ggs_usr_fk", "gg_struct", ["user_nm"], unique=False)
    op.alter_column(
        "gg_struct",
        "ts_mut",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=None,
        existing_comment="Tijdstip laatste mutatie",
        existing_nullable=False,
    )
    op.alter_column(
        "gg_struct",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default=None,
        comment="User identification.",
        existing_comment="User identification",
        existing_nullable=False,
    )
    op.alter_column(
        "gg",
        "ts_mut",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=None,
        existing_comment="Tijdstip laatste mutatie",
        existing_nullable=False,
    )
    op.alter_column(
        "gg",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default=None,
        comment="User identification.",
        existing_comment="User identification",
        existing_nullable=False,
    )
    op.drop_constraint(op.f("fk_evtp_version_evtp_cd_evtp"), "evtp_version", type_="foreignkey")
    op.drop_index(op.f("ix_evtp_version_evtp_cd"), table_name="evtp_version")
    op.alter_column(
        "evtp_version",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default=None,
        comment=None,
        existing_comment="User identification",
        existing_nullable=False,
    )
    op.alter_column(
        "evtp_ond",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default=None,
        existing_comment="User identification",
        existing_nullable=False,
    )
    op.alter_column(
        "evtp_oe_com_type",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default=sa.text("'PVZ'::character varying"),
        existing_comment="User identification",
        existing_nullable=False,
    )
    op.alter_column(
        "evtp_gst",
        "ts_mut",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=None,
        existing_comment="Tijdstip laatste mutatie",
        existing_nullable=False,
    )
    op.alter_column(
        "evtp_gst",
        "user_nm",
        existing_type=sa.VARCHAR(length=30),
        server_default=sa.text("'PVZ'::character varying"),
        existing_comment="User identification",
        existing_nullable=False,
    )
    # ### end Alembic commands ###
