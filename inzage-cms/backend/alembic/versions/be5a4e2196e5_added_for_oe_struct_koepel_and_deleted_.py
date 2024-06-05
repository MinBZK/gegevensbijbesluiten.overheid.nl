"""added for oe_struct koepel and deleted ibron

Revision ID: be5a4e2196e5
Revises: 364cc98491ea
Create Date: 2024-03-29 11:09:19.773687

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "be5a4e2196e5"
down_revision = "364cc98491ea"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("oe_struct", sa.Column("koepel", sa.Boolean(), nullable=True, comment="Wel of koepel"))
    op.drop_column("oe_struct", "ibron_cd")


def downgrade() -> None:
    op.drop_column("oe_struct", "koepel")
    op.add_column("oe_struct", sa.Column("ibron_cd", sa.Integer(), nullable=True, comment="Wel of ibron"))
    op.create_foreign_key(op.f("fk_ibron_ibron_cd_ibron"), "oe_struct", "ibron", ["ibron_cd"], ["ibron_cd"])
