"""add sortering into gst_gg_rge

Revision ID: 4d3b495ccce3
Revises: e4d56dca11fa
Create Date: 2023-05-08

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "4d3b495ccce3"
down_revision = "e4d56dca11fa"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("gst_gg_rge", sa.Column("sort_key", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("gst_gg_rge", "sort_key")
