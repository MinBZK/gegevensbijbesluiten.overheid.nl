"""added foreign keys to evtp table

Revision ID: e061c5d0b42d
Revises: 74062a029409
Create Date: 2024-05-13 21:37:45.903392

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "e061c5d0b42d"
down_revision = "74062a029409"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_foreign_key("fk_evtp_acc_evtp", "evtp_acc", "evtp", ["evtp_cd"], ["evtp_cd"])
    op.create_foreign_key("fk_evtp_gst_evtp", "evtp_gst", "evtp", ["evtp_cd"], ["evtp_cd"])
    op.create_foreign_key("fk_evtp_version_evtp_sup", "evtp_version", "evtp", ["evtp_cd_sup"], ["evtp_cd"])
    op.create_foreign_key("fk_evtp_oe_com_type_evtp", "evtp_oe_com_type", "evtp", ["evtp_cd"], ["evtp_cd"])
    op.create_foreign_key("fk_evtp_ond_evtp", "evtp_ond", "evtp", ["evtp_cd"], ["evtp_cd"])


def downgrade() -> None:
    op.drop_constraint("fk_evtp_acc_evtp", "evtp_acc", type_="foreignkey")
    op.drop_constraint("fk_evtp_gst_evtp", "evtp_gst", type_="foreignkey")
    op.drop_constraint("fk_evtp_version_evtp_sup", "evtp_version", type_="foreignkey")
    op.drop_constraint("fk_evtp_oe_com_type_evtp", "evtp_oe_com_type", type_="foreignkey")
    op.drop_constraint("fk_evtp_ond_evtp", "evtp_ond", type_="foreignkey")
