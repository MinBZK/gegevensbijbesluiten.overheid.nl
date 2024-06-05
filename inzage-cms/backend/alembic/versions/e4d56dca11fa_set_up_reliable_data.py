"""set up reliable data

Revision ID: e4d56dca11fa
Revises: 962fd6ab7f10
Create Date: 2023-04-03 12:04:15.283159

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "e4d56dca11fa"
down_revision = "962fd6ab7f10"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with open("app/database/setup/1.set_up_data.sql") as file:
        op.execute(file.read())


def downgrade() -> None:
    tables = [
        "gst_gstt",
        "gst_gg_rge",
        "gg_struct",
        "oe_struct",
        "oe_struct_rolt",
        "evtp_acc",
        "evtp_gst",
        "oe_type",
        "rge",
        "evtp",
        "gg",
        "gst_type",
        "gst",
        "oe",
        "ibron",
        "bestand_acc",
        "tabellenvoorbeheer",
        "rubriekenvoorbeheer",
        "persoon",
        "evtp_version",
    ]

    [op.execute(f"delete from {table} cascade") for table in tables]
