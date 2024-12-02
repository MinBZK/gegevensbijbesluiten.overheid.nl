"""deleted evtp_cd_sup

Revision ID: ea59c84f381b
Revises: 0a03d9a9aa0f
Create Date: 2024-11-12 14:54:16.977073

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ea59c84f381b"
down_revision = "0a03d9a9aa0f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("evtp_version", "evtp_cd_sup")


def downgrade() -> None:
    op.add_column("evtp_version", sa.Column("evtp_cd_sup", sa.INTEGER(), nullable=True, comment="Koepelbesluit"))
