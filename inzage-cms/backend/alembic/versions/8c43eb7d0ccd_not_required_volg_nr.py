"""not_required_volg_nr

Revision ID: 8c43eb7d0ccd
Revises: 0e02e925efeb
Create Date: 2024-07-02 13:30:00.547047

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "8c43eb7d0ccd"
down_revision = "0e02e925efeb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("evtp_acc", "volg_nr", nullable=True)


def downgrade() -> None:
    op.execute("UPDATE evtp_acc SET volg_nr=-1 WHERE volg_nr IS NULL")
    op.alter_column("evtp_acc", "volg_nr", nullable=False, existing_server_default="0")
