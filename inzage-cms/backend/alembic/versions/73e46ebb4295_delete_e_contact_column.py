"""delete e_contact column

Revision ID: 73e46ebb4295
Revises: 0b095f0dc494
Create Date: 2024-09-02 14:38:12.965409

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "73e46ebb4295"
down_revision = "0b095f0dc494"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("oe", "e_contact")


def downgrade() -> None:
    op.add_column("oe", sa.Column("e_contact", sa.String(length=200), nullable=True))
