"""delete_or_struct

Revision ID: 4707766c4c6e
Revises: cfe63fc75179
Create Date: 2024-06-06 09:55:27.789430

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "4707766c4c6e"
down_revision = "cfe63fc75179"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_table("oe_struct")
    op.create_table(
        "oe_koepel",
        sa.Column(
            "titel",
            sa.VARCHAR(length=255),
            autoincrement=False,
            nullable=False,
            comment="Titel van de koepelorganisatie",
        ),
        sa.Column(
            "omschrijving",
            sa.VARCHAR(length=4000),
            autoincrement=False,
            nullable=False,
            comment="Omschrijving van de koepelorganisatie",
        ),
        sa.Column("oe_koepel_cd", sa.INTEGER(), autoincrement=True, nullable=False, comment="Koepel organisatie code"),
        sa.Column(
            "ts_start",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("'2023-01-01 00:00:00+00'::timestamp with time zone"),
            autoincrement=False,
            nullable=False,
            comment="Tijdstip start datum",
        ),
        sa.Column(
            "ts_end",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("'9999-12-31 23:59:59.999999+00'::timestamp with time zone"),
            autoincrement=False,
            nullable=False,
            comment="Tijdstip einde datum",
        ),
        sa.Column(
            "user_nm",
            sa.VARCHAR(length=30),
            server_default=sa.text("'ICTU'::character varying"),
            autoincrement=False,
            nullable=True,
            comment="Gebruikersnaam",
        ),
        sa.Column(
            "ts_mut",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
            comment="Tijdstip laatste mutatie",
        ),
        sa.Column("notitie", sa.VARCHAR(length=4000), autoincrement=False, nullable=True, comment="Notitieveld"),
        sa.PrimaryKeyConstraint("oe_koepel_cd", name="oe_koepel_pkey"),
        comment="Overkoepelende organisatie",
    )

    op.create_table(
        "oe_koepel_oe",
        sa.Column(
            "oe_koepel_oe_cd",
            sa.INTEGER(),
            autoincrement=True,
            nullable=False,
            comment="koppeling koepel organisatie code",
        ),
        sa.Column("oe_cd", sa.INTEGER(), autoincrement=False, nullable=False, comment="Organisatie code"),
        sa.Column("oe_koepel_cd", sa.INTEGER(), autoincrement=False, nullable=False, comment="Koepel organisatie code"),
        sa.Column(
            "ts_start",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("'2023-01-01 00:00:00+00'::timestamp with time zone"),
            autoincrement=False,
            nullable=False,
            comment="Tijdstip start datum",
        ),
        sa.Column(
            "ts_end",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("'9999-12-31 23:59:59.999999+00'::timestamp with time zone"),
            autoincrement=False,
            nullable=False,
            comment="Tijdstip einde datum",
        ),
        sa.Column(
            "user_nm",
            sa.VARCHAR(length=30),
            server_default=sa.text("'ICTU'::character varying"),
            autoincrement=False,
            nullable=True,
            comment="Gebruikersnaam",
        ),
        sa.Column(
            "ts_mut",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
            comment="Tijdstip laatste mutatie",
        ),
        sa.Column("notitie", sa.VARCHAR(length=4000), autoincrement=False, nullable=True, comment="Notitieveld"),
        sa.ForeignKeyConstraint(["oe_cd"], ["oe.oe_cd"], name="oe_koepel_oe_koepel_fk"),
        sa.ForeignKeyConstraint(["oe_koepel_cd"], ["oe_koepel.oe_koepel_cd"], name="oe_koepel_oe_oe_fk"),
        sa.PrimaryKeyConstraint("oe_koepel_oe_cd", name="oe_koepel_oe_pkey"),
        comment="Koppeling tussen koepel organisaties en organisaties",
    )


def downgrade() -> None:
    op.create_table(
        "oe_struct",
        sa.Column(
            "user_nm",
            sa.VARCHAR(length=30),
            server_default=sa.text("'ICTU'::character varying"),
            autoincrement=False,
            nullable=True,
            comment="Gebruikersnaam",
        ),
        sa.Column("notitie", sa.VARCHAR(length=4000), autoincrement=False, nullable=True, comment="Notitieveld"),
        sa.Column(
            "ts_mut",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
            comment="Tijdstip laatste mutatie",
        ),
        sa.Column(
            "oe_cd_sub", sa.INTEGER(), autoincrement=False, nullable=False, comment="Sub (child) organisatie code"
        ),
        sa.Column(
            "oe_cd_sup", sa.INTEGER(), autoincrement=False, nullable=False, comment="Sup (parent) organisatie code"
        ),
        sa.Column(
            "oe_struct_cd", sa.INTEGER(), autoincrement=True, nullable=False, comment="Organisatie structuur code"
        ),
        sa.Column(
            "ts_start",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("'2023-01-01 00:00:00+00'::timestamp with time zone"),
            autoincrement=False,
            nullable=False,
            comment="Tijdstip start datum",
        ),
        sa.Column(
            "ts_end",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("'9999-12-31 23:59:59.999999+00'::timestamp with time zone"),
            autoincrement=False,
            nullable=False,
            comment="Tijdstip einde datum",
        ),
        sa.Column("koepel", sa.BOOLEAN(), autoincrement=False, nullable=True, comment="Wel of koepel"),
        sa.ForeignKeyConstraint(["oe_cd_sub"], ["oe.oe_cd"], name="oes_oe_sub_fk"),
        sa.ForeignKeyConstraint(["oe_cd_sup"], ["oe.oe_cd"], name="oes_oe_sup_fk"),
        sa.PrimaryKeyConstraint("oe_struct_cd", name="oe_struct_pkey"),
        comment="Hiërarchische structuur van organisaties wat resulteert in een sub(=child)-sup(=parent) relatie",
    )
    op.drop_constraint(op.f("oe_koepel_oe_koepel_fk"), "oe_koepel_oe", type_="foreignkey")
    op.drop_constraint(op.f("oe_koepel_oe_oe_fk"), "oe_koepel_oe", type_="foreignkey")

    op.drop_table("oe_koepel")
    op.drop_table("oe_koepel_oe")
