"""added toelichting field and swapped with notitie

Revision ID: 039b1c30b48f
Revises: ea59c84f381b
Create Date: 2024-11-25 16:37:14.042397

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "039b1c30b48f"
down_revision = "ea59c84f381b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "oe",
        sa.Column("toelichting", sa.String(length=4000), nullable=True, comment="Toelichting"),
    )
    op.execute(
        """
        UPDATE oe
        SET toelichting = notitie;

        UPDATE oe
        SET notitie = null;
    """
    )


def downgrade() -> None:
    op.drop_column("oe", "toelichting")
