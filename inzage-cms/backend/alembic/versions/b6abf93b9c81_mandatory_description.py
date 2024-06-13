"""mandatory_description

Revision ID: b6abf93b9c81
Revises: e061c5d0b42d
Create Date: 2024-05-16 13:09:14.264556

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "b6abf93b9c81"
down_revision = "e061c5d0b42d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE evtp_version
        SET omschrijving = 'nog in te vullen'
        WHERE omschrijving IN ('xx', 'todo', '????', '', ' ', '  ', '   ', NULL)
        ;
    """
    )
    op.alter_column(
        "evtp_version",
        "omschrijving",
        nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "evtp_version",
        "omschrijving",
        nullable=True,
    )
