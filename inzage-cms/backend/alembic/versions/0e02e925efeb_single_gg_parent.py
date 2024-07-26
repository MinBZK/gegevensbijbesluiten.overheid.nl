"""single_gg_parent

Revision ID: 0e02e925efeb
Revises: 4707766c4c6e
Create Date: 2024-07-02 10:46:57.753350

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "0e02e925efeb"
down_revision = "4707766c4c6e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint(constraint_name="uq_gg_cd_sub", table_name="gg_struct", columns=["gg_cd_sub"])


def downgrade() -> None:
    op.drop_constraint(constraint_name="uq_gg_cd_sub", table_name="gg_struct", type_="unique")
