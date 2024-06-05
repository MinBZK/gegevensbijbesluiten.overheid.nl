"""types in oe

Revision ID: 96858896134e
Revises: 4d3b495ccce3
Create Date: 2023-05-26 13:54:02.201532

"""

from alembic import op
from sqlalchemy import BIGINT, VARCHAR

# revision identifiers, used by Alembic.
revision = "96858896134e"
down_revision = "4d3b495ccce3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "oe",
        "lidw_sgebr",
        nullable=True,
    )
    op.alter_column("oe", "fax", type_=VARCHAR(30))


def downgrade() -> None:
    op.alter_column("oe", "fax", type_=BIGINT, postgresql_using="fax::bigint")
