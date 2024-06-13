"""added uri

Revision ID: 74062a029409
Revises: f44ff3a38f3f
Create Date: 2024-04-24 14:52:53.975433

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "74062a029409"
down_revision = "f44ff3a38f3f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "evtp_version",
        sa.Column("uri", sa.String(length=200), nullable=True, comment="Uniform resource identifier voor een besluit"),
    )
    with open("app/database/setup/3.set_up_latest_changes.sql") as file:
        op.execute(file.read())


def downgrade() -> None:
    op.drop_column("evtp_version", "uri")
