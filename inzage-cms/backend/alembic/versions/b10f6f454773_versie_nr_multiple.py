"""versie_nr_multiple

Revision ID: b10f6f454773
Revises: b6abf93b9c81
Create Date: 2024-05-06 15:20:56.342227

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b10f6f454773"
down_revision = "b6abf93b9c81"
branch_labels = None
depends_on = None


def upgrade() -> None:
    def new_evtp_xx(table: str, comment: str):
        op.add_column(table, sa.Column("versie_nr", sa.INTEGER(), nullable=True, comment=comment))
        op.execute(
            f"""
            UPDATE {table}
            SET versie_nr = COALESCE((
                SELECT MAX(evtp_version.versie_nr)
                FROM evtp_version
                WHERE
                    {table}.evtp_cd = evtp_version.evtp_cd
                    AND {table}.ts_start < evtp_version.ts_end
                    AND {table}.ts_end > evtp_version.ts_start
            ), 0);
        """
        )
        op.alter_column(table, "versie_nr", nullable=False)

    new_evtp_xx("evtp_gst", comment="versienummer van het gerelateerde besluit")
    new_evtp_xx("evtp_oe_com_type", comment="versienummer van het gerelateerde besluit")
    new_evtp_xx("evtp_ond", comment="versienummer van het gerelateerde besluit")

    def new_gst_xx(table: str, comment: str):
        op.add_column(table, sa.Column("versie_nr", sa.INTEGER(), nullable=True, comment=comment))
        op.execute(
            f"""
            UPDATE {table}
            SET versie_nr = COALESCE((
                SELECT MAX(evtp_version.versie_nr)
                FROM evtp_version
                INNER JOIN evtp_gst ON evtp_version.evtp_cd = evtp_gst.evtp_cd
                WHERE
                    {table}.gst_cd = evtp_gst.gst_cd
                    AND {table}.ts_start < evtp_version.ts_end
                    AND {table}.ts_end > evtp_version.ts_start
            ), 0);
        """
        )
        op.alter_column(table, "versie_nr", nullable=False)

    new_gst_xx("gst_gstt", comment="versienummer van het gerelateerde besluit")
    new_gst_xx("gst_gg", comment="versienummer van het gerelateerde besluit")
    new_gst_xx("gst_rge", comment="versienummer van het gerelateerde besluit")


def downgrade() -> None:
    op.drop_column("evtp_gst", "versie_nr")
    op.drop_column("evtp_oe_com_type", "versie_nr")
    op.drop_column("evtp_ond", "versie_nr")
    op.drop_column("gst_gstt", "versie_nr")
    op.drop_column("gst_gg", "versie_nr")
    op.drop_column("gst_rge", "versie_nr")
