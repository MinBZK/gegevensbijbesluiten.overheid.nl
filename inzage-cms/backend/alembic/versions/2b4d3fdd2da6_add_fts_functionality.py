"""add fts functionality

Revision ID: 2b4d3fdd2da6
Revises: 73e46ebb4295
Create Date: 2024-09-05 10:48:39.252733

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "2b4d3fdd2da6"
down_revision = "73e46ebb4295"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with open("app/database/full_text_search/0.init.sql") as file:
        op.execute(file.read())
    with open("app/database/full_text_search/1.create_vector_column.sql") as file:
        op.execute(file.read())
    with open("app/database/full_text_search/2.abb_dictionary.sql") as file:
        op.execute(file.read())
    with open("app/database/full_text_search/3.create_words_table.sql") as file:
        op.execute(file.read())


def downgrade() -> None:
    with open("app/database/full_text_search/4.remove_words_table.sql") as file:
        op.execute(file.read())
    with open("app/database/full_text_search/5.remove_vectorized_column.sql") as file:
        op.execute(file.read())
