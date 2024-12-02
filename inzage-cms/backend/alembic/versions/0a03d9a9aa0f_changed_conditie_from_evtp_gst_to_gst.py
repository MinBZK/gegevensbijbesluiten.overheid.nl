"""changed conditie from evtp_gst to gst

Revision ID: 0a03d9a9aa0f
Revises: 2b4d3fdd2da6
Create Date: 2024-11-05 10:27:15.723038

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0a03d9a9aa0f"
down_revision = "2b4d3fdd2da6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "gst",
        sa.Column(
            "conditie",
            sa.VARCHAR(length=4000),
            nullable=True,
            comment="Toelichting van een conditie waaronder de gegevensstroom plaatsvindt, bijvoorbeeld ziek worden, wel of geen werk hebben, etc.",
        ),
    )
    op.execute(
        """
        -- insert conditie into new column conditie in gst
        WITH conditie_evtp_gst as (
            SELECT eg.evtp_cd, eg.gst_cd, eg.conditie
            FROM evtp_gst eg
            WHERE eg.ts_end > to_date('9999-12-31', 'YYYY-MM-DD')
            GROUP BY eg.evtp_cd, eg.gst_cd, eg.conditie
        )
        UPDATE gst
        SET conditie = conditie_evtp_gst.conditie
        FROM conditie_evtp_gst
        WHERE conditie_evtp_gst.gst_cd = gst.gst_cd;
        """
    )
    op.drop_column("evtp_gst", "conditie")


def downgrade() -> None:
    op.add_column(
        "evtp_gst",
        sa.Column(
            "conditie",
            sa.VARCHAR(length=4000),
            nullable=True,
            comment="Toelichting van een conditie waaronder de gegevensstroom plaatsvindt, bijvoorbeeld ziek worden, wel of geen werk hebben, etc.",
        ),
    )
    op.drop_column("gst", "conditie")
