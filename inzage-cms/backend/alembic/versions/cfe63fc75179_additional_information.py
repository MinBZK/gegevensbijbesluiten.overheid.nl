"""additional_information

Revision ID: cfe63fc75179
Revises: b10f6f454773
Create Date: 2024-05-30 13:13:09.999222

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "cfe63fc75179"
down_revision = "b10f6f454773"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "evtp_version",
        sa.Column(
            "overige_informatie", sa.String(length=4000), nullable=True, comment="Extra informatie over het besluit"
        ),
    )
    op.add_column(
        "evtp_version",
        sa.Column(
            "overige_informatie_link",
            sa.String(length=2000),
            nullable=True,
            comment="Link naar extra informatie over het besluit",
        ),
    )


def downgrade() -> None:
    op.drop_column("evtp_version", "overige_informatie")
    op.drop_column("evtp_version", "overige_informatie_link")
