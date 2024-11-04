"""adjusted ibron table

Revision ID: 0b095f0dc494
Revises: f0b292ced71a
Create Date: 2024-08-19 15:40:15.139750

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0b095f0dc494"
down_revision = "f0b292ced71a"
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns
    op.add_column(
        "ibron",
        sa.Column(
            "titel",
            sa.VARCHAR(length=200),
            nullable=False,
            server_default="ICTU",
            comment="Titel van de informatiebron",
        ),
    )
    op.add_column(
        "ibron", sa.Column("afko", sa.VARCHAR(length=15), nullable=True, comment="Afkorting van de informatiebron")
    )
    op.add_column("ibron", sa.Column("lidw", sa.VARCHAR(length=12), nullable=True, comment="Lidwoord code van de bron"))
    op.add_column(
        "ibron", sa.Column("link", sa.VARCHAR(length=200), nullable=True, comment="Link naar de informatiebron")
    )
    op.alter_column(
        "ibron",
        "oe_cd",
        existing_type=sa.Integer(),
        nullable=False,
        comment="Organisatie die de informatiebron beheert",
    )
    op.drop_column("ibron", "omschrijving")
    op.execute(
        "COMMENT ON TABLE ibron IS 'registers, administraties, systemen etc. waarin gegevens worden beheerd door een organisatie'"
    )
    op.execute(
        """
        --- add new/enriched infobron records
        INSERT INTO ibron (titel, afko, lidw, link, oe_cd, notitie, user_nm, ts_mut, ts_start, ts_end)
        SELECT naam_officieel, afko, lidw_sgebr, e_contact, oe_cd, notitie, user_nm, ts_mut, ts_start, ts_end
        FROM oe
        WHERE oe_cd IN (
        SELECT oe_cd FROM ibron
        );

        -- update all ibron_cd keys in gst in the gst with the new ones
        WITH updated_gst AS (
            SELECT g.gst_cd, i2.ibron_cd AS new_ibron_cd
            FROM gst g
            JOIN oe ON oe.oe_cd = g.oe_bron
            JOIN ibron i ON i.ibron_cd = g.ibron_cd
            JOIN oe oe2 ON oe2.oe_cd = i.oe_cd
            JOIN ibron i2 ON i2.titel = oe2.naam_officieel
            WHERE g.ibron_cd IS NOT NULL
        )
        UPDATE gst
        SET ibron_cd = updated_gst.new_ibron_cd
        FROM updated_gst
        WHERE gst.gst_cd = updated_gst.gst_cd;


        -- insert new ibron_cd in gst WHERE the oe_bron has a ibron
        WITH updated_gst AS (
            SELECT g.gst_cd, g.ibron_cd as g_ibron_cd, g.oe_bron as bron_oe_cd, oe.ibron_cd as oe_bron_cd, i2.ibron_cd as new_ibron_cd
            FROM gst g
            JOIN oe on oe.oe_cd = g.oe_bron
            JOIN ibron i on i.ibron_cd = oe.ibron_cd
            JOIN oe oe2 on oe2.oe_cd = i.oe_cd
            JOIN ibron i2 on i2.titel = oe2.naam_officieel
            WHERE g.ibron_cd is null
        )
        UPDATE gst
        SET ibron_cd = updated_gst.new_ibron_cd
        FROM updated_gst
        WHERE gst.gst_cd = updated_gst.gst_cd;

        -- set the responsible organisation back to ibron
        WITH updated_oe as (
            SELECT oe.oe_cd, oe.ibron_cd, oe.naam_officieel
            FROM oe
            WHERE oe.ibron_cd is not null
        )
        UPDATE ibron
        SET oe_cd = updated_oe.oe_cd
        FROM updated_oe
        WHERE ibron.titel = updated_oe.naam_officieel;

        WITH updated_ibron as (
            SELECT oe.oe_cd as oe_naam_officieel, oe.naam_officieel, i.oe_cd as ibron_oe_cd, i.ibron_cd as old_ibron_cd, i.titel, oe2.naam_officieel
            FROM ibron i
            JOIN oe on i.ibron_cd = oe.ibron_cd
            JOIN oe oe2 on oe2.oe_cd = i.oe_cd
        )
        UPDATE ibron
        SET oe_cd = updated_ibron.oe_naam_officieel
        FROM updated_ibron
        WHERE ibron.oe_cd = updated_ibron.ibron_oe_cd
        AND ibron.titel != 'ICTU';
        """
    )
    op.drop_constraint("oe_ibrn_fk", "oe", type_="foreignkey")
    op.drop_column("oe", "ibron_cd")
    op.execute(
        """
        -- delete all old ibron pk in ibron
        DELETE FROM ibron WHERE titel='ICTU';
               """
    )


def downgrade():
    op.execute("COMMENT ON TABLE ibron IS 'register waar de gegevens afkomstig van zijn'")
    op.add_column(
        "ibron", sa.Column("omschrijving", sa.VARCHAR(length=80), nullable=True, comment="Omschrijving van de bron")
    )
    op.alter_column("ibron", "oe_cd", existing_type=sa.Integer(), nullable=True, comment="Organisatie code")
    op.drop_column("ibron", "link")
    op.drop_column("ibron", "lidw")
    op.drop_column("ibron", "afko")
    op.drop_column("ibron", "titel")
    op.add_column("oe", sa.Column("ibron_cd", sa.Integer(), nullable=False, comment="Informatiebroncode"))
    op.create_foreign_key("oe_ibrn_fk", "oe", "ibron", ["ibron_cd"], ["ibron_cd"])
