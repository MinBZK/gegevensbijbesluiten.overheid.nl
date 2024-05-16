"""First setup inzage db

Revision ID: 962fd6ab7f10
Revises:
Create Date: 2023-02-27 17:46:03.397124

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "962fd6ab7f10"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    with open("app/database/setup/0.set_up_schema.sql") as file:
        op.execute(file.read())


def downgrade() -> None:
    tables = [
        "evtp",
        "gg",
        "oe",
        "bestand_acc",
        "evtp_acc",
        "evtp_gst",
        "gst",
        "ibron",
        "gg_struct",
        "gst_gg_rge",
        "rge",
        "gst_gstt",
        "gst_type",
        "oe_struct",
        "oe_struct_rolt",
        "oe_type",
        "tabellenvoorbeheer",
        "rubriekenvoorbeheer",
        "persoon",
        "evtp_version",
    ]
    [op.execute(f"drop table {table} cascade") for table in tables]
