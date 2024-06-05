"""generate oe upc

Revision ID: 0836fc8fa349
Revises: 6887445da1f5
Create Date: 2024-02-28 13:19:45.887522

"""

import sqlalchemy as sa
from alembic import op
from numpy import random

# revision identifiers, used by Alembic.
revision = "0836fc8fa349"
down_revision = "6887445da1f5"
branch_labels = None
depends_on = None


def create_upc():
    rl = []
    upc = ""
    for _ in range(0, 7):
        n = random.randint(0, 9)
        # Ensure the first digit is not 0
        if _ == 0 and n == 0:
            n = random.randint(1, 9)
        rl.append(str(n))
    e = int(rl[0]) + int(rl[2]) + int(rl[4]) + int(rl[6])
    o = int(rl[1]) + int(rl[3]) + int(rl[5])
    c = (e * 3 + o) % 10
    rl.append(str(c))
    return upc.join(rl)


def upgrade() -> None:
    # Connect to the database engine
    op.add_column("oe", sa.Column("oe_upc", sa.Integer(), nullable=True))
    connection = op.get_bind()
    oe_table = sa.Table("oe", sa.MetaData(), autoload_with=connection)
    rows = connection.execute(sa.select(oe_table)).fetchall()

    # Iterate through each row and generate unique UPC
    upc_list = []
    for row in rows:
        while True:
            unique_upc = create_upc()
            if unique_upc not in upc_list:
                upc_list.append(unique_upc)
                break

        # Update the row with the generated UPC
        connection.execute(oe_table.update().where(oe_table.c.oe_cd == row.oe_cd).values(oe_upc=unique_upc))


def downgrade() -> None:
    op.drop_column("oe", "oe_upc")
