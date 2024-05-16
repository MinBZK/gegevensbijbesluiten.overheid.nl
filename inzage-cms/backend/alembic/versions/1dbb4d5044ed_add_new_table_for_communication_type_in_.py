"""add new table for communication type in oe

Revision ID: 1dbb4d5044ed
Revises: 96858896134e
Create Date: 2023-06-05 10:55:59.208828

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "1dbb4d5044ed"
down_revision = "96858896134e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "oe_com_type",
        sa.Column(
            "oe_com_type_cd",
            sa.Integer(),
            primary_key=True,
            autoincrement=True,
            comment="Kanaal type code",
        ),
        sa.Column(
            "omschrijving",
            sa.VARCHAR(4000),
            nullable=False,
            comment="Omschrijving van het kanaal",
        ),
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
            nullable=False,
            comment="Tijdstip laatste mutatie",
        ),
        comment="Communicatie kanalen die gebruikt worden door organisaties",
    )
    op.create_table(
        "evtp_oe_com_type",
        sa.Column(
            "evtp_oe_com_type_cd",
            sa.Integer(),
            primary_key=True,
            autoincrement=True,
            comment="Besluit organisatie code",
        ),
        sa.Column(
            "evtp_cd",
            sa.Integer(),
            sa.ForeignKey("evtp.evtp_cd", name="evtp_oe_com_evtp_fk"),
            nullable=False,
            comment="Eventtype code",
        ),
        sa.Column(
            "oe_com_type_cd",
            sa.Integer(),
            sa.ForeignKey(
                "oe_com_type.oe_com_type_cd",
                name="evtp_oe_com_type_oe_com_type_fk",
            ),
            nullable=False,
            comment="Kanaal type code",
        ),
        sa.Column(
            "link",
            sa.VARCHAR(2000),
            nullable=True,
            comment="Hyperlink waar de burger de uitkomst van het besluit ontvangt",
        ),
        comment="Relatie tussen besluit en bestemming organiatie communicatie kanaal",
    )

    # Include comment on new column in revision 4d3b495ccce3
    op.alter_column(
        "gst_gg_rge",
        "sort_key",
        comment="Sorteersleutel van het gegevensgroep in het gegevensstroom blokje",
    )


def downgrade() -> None:
    op.drop_table("evtp_oe_com_type")
    op.drop_table("oe_com_type")
