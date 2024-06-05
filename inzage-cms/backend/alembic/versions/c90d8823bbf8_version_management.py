"""version management

Revision ID: c90d8823bbf8
Revises: 1dbb4d5044ed
Create Date: 2023-09-05 05:16:42.270907

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c90d8823bbf8"
down_revision = "1dbb4d5044ed"
branch_labels = None
depends_on = None


# Define the upgrade and downgrade operations
def upgrade():
    # Step 1: Create evtp_version table
    op.create_table(
        "evtp_version",
        sa.Column("evtp_cd", sa.Integer(), nullable=False),
        sa.Column("versie_nr", sa.Integer(), nullable=False),
        sa.Column("evtp_nm", sa.String(length=200), nullable=False),
        sa.Column("omschrijving", sa.String(length=2000)),
        sa.Column("user_nm", sa.String(length=30), nullable=False),
        sa.Column("notitie", sa.String(length=4000)),
        sa.Column("evtp_cd_sup", sa.Integer()),
        sa.Column("oe_best", sa.Integer()),
        sa.Column("aanleiding", sa.String(length=2000), nullable=False),
        sa.Column("gebr_dl", sa.String(length=200), nullable=False),
        sa.Column("lidw_soort_besluit", sa.String(length=12)),
        sa.Column("soort_besluit", sa.String(length=50)),
        sa.Column("id_publicatiestatus", sa.Integer(), nullable=False),
        sa.Column(
            "ts_mut",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "ts_start",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'2023-01-01'"),
        ),
        sa.Column(
            "ts_end",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'9999-12-31 23:59:59.999999+00'"),
        ),
        sa.Column("huidige_versie", sa.Boolean(), server_default=sa.text("false")),
        sa.PrimaryKeyConstraint("evtp_cd", "versie_nr"),
    )

    op.create_index("idx_17910_version_oe_fk", "evtp_version", ["oe_best"])
    op.create_index("idx_18001_version_evtp_fk", "evtp_version", ["evtp_cd"])

    op.create_foreign_key(
        "evpt_evptsup_fk",
        "evtp_version",
        "evtp",
        ["evtp_cd_sup"],
        ["evtp_cd"],
        onupdate="NO ACTION",
        ondelete="CASCADE",
    )

    op.create_foreign_key(
        "evpt_oe_fk",
        "evtp_version",
        "oe",
        ["oe_best"],
        ["oe_cd"],
        onupdate="NO ACTION",
        ondelete="CASCADE",
    )

    # Step 2: Inject data into evtp_version
    op.execute(
        """
        INSERT INTO evtp_version(evtp_cd, versie_nr, evtp_nm, omschrijving, user_nm, notitie, evtp_cd_sup, oe_best, aanleiding, gebr_dl, lidw_soort_besluit, soort_besluit, id_publicatiestatus, ts_mut, ts_start, ts_end, huidige_versie)
        SELECT evtp_cd, 1, evtp_nm, omschrijving, user_nm, notitie, evtp_cd_sup, oe_best, aanleiding, gebr_dl, lidw_soort_besluit, soort_besluit, id_publicatiestatus, ts_mut, '2023-01-01', '9999-12-31 23:59:59.999999+00', true
        FROM evtp;
    """
    )

    # Step 3: Update the publicatienumbers from evtps
    op.execute(
        """
        UPDATE evtp_version
        SET id_publicatiestatus = CASE
            WHEN id_publicatiestatus IN (1, 2) THEN 1
            WHEN id_publicatiestatus IN (3, 4) THEN 2
            WHEN id_publicatiestatus = 5 THEN 3
            WHEN id_publicatiestatus = 6 THEN 4
            ELSE id_publicatiestatus
        END;
    """
    )

    # Step 4: Trim the EVTP table
    op.drop_column("evtp", "evtp_nm")
    op.drop_column("evtp", "omschrijving")
    op.drop_column("evtp", "user_nm")
    op.drop_column("evtp", "notitie")
    op.drop_column("evtp", "evtp_cd_sup")
    op.drop_column("evtp", "srt_event")
    op.drop_column("evtp", "oe_best")
    op.drop_column("evtp", "aanleiding")
    op.drop_column("evtp", "gebr_dl")
    op.drop_column("evtp", "ind_pilot")
    op.drop_column("evtp", "sort_key")
    op.drop_column("evtp", "gg_cd")
    op.drop_column("evtp", "lidw_soort_besluit")
    op.drop_column("evtp", "soort_besluit")
    op.drop_column("evtp", "id_publicatiestatus")
    op.drop_column("evtp", "ts_mut")

    # Step 5: change type of evtp_upc and gst_upc to integer
    # Create a new temporary column
    op.add_column("evtp", sa.Column("evtp_upc_temp", sa.Integer(), nullable=True))
    op.add_column("gst", sa.Column("gst_upc_temp", sa.Integer(), nullable=True))

    # Copy and convert the data from the old column to the new column
    op.execute("""UPDATE evtp SET evtp_upc_temp = CAST(evtp_upc AS INTEGER)""")
    op.execute("""UPDATE gst SET gst_upc_temp = CAST(gst_upc AS INTEGER)""")

    # Drop the old column
    op.drop_column("evtp", "evtp_upc")
    op.drop_column("gst", "gst_upc")

    # Rename the new column to the old column's name
    op.execute("""ALTER TABLE evtp RENAME COLUMN evtp_upc_temp TO evtp_upc""")
    op.execute("""ALTER TABLE gst RENAME COLUMN gst_upc_temp TO gst_upc""")

    # Step 6: add columns and set default values for the specified tables
    op.add_column(
        "evtp_gst",
        sa.Column(
            "ts_start",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'2023-01-01'"),
        ),
    )
    op.add_column(
        "evtp_gst",
        sa.Column(
            "ts_end",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'9999-12-31 23:59:59.999999+00'"),
        ),
    )

    op.drop_column("gg", "sys_nm")
    op.drop_column("gg", "col_nm")
    op.drop_column("gg", "rt_nm")
    op.drop_column("gg", "dom_nm")
    op.drop_column("gg", "ind_pilot")

    op.add_column("gg", sa.Column("koepel", sa.Boolean()))
    op.add_column(
        "gg",
        sa.Column(
            "ts_start",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'2023-01-01'"),
        ),
    )
    op.add_column(
        "gg",
        sa.Column(
            "ts_end",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'9999-12-31 23:59:59.999999+00'"),
        ),
    )

    op.drop_column("gst", "ind_pilot")

    op.add_column(
        "gst",
        sa.Column(
            "ts_start",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'2023-01-01'"),
        ),
    )
    op.add_column(
        "gst",
        sa.Column(
            "ts_end",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'9999-12-31 23:59:59.999999+00'"),
        ),
    )

    op.drop_column("gst_type", "sort_key")

    op.add_column(
        "gst_type",
        sa.Column(
            "ts_start",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'2023-01-01'"),
        ),
    )
    op.add_column(
        "gst_type",
        sa.Column(
            "ts_end",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'9999-12-31 23:59:59.999999+00'"),
        ),
    )

    op.drop_column("oe", "ind_brf")
    op.drop_column("oe", "srt_brf")
    op.drop_column("oe", "ind_gebr")
    op.drop_column("oe", "ind_pilot")
    op.drop_column("oe", "e_contact_omschrijving")

    op.add_column(
        "oe",
        sa.Column(
            "ts_start",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'2023-01-01'"),
        ),
    )
    op.add_column(
        "oe",
        sa.Column(
            "ts_end",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'9999-12-31 23:59:59.999999+00'"),
        ),
    )

    op.drop_column("oe_type", "get_label")
    op.drop_column("oe_type", "icout_id")

    op.add_column(
        "oe_type",
        sa.Column(
            "ts_start",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'2023-01-01'"),
        ),
    )
    op.add_column(
        "oe_type",
        sa.Column(
            "ts_end",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'9999-12-31 23:59:59.999999+00'"),
        ),
    )

    op.add_column(
        "oe_com_type",
        sa.Column(
            "ts_start",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'2023-01-01'"),
        ),
    )
    op.add_column(
        "oe_com_type",
        sa.Column(
            "ts_end",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'9999-12-31 23:59:59.999999+00'"),
        ),
    )

    op.add_column(
        "ibron",
        sa.Column(
            "ts_start",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'2023-01-01'"),
        ),
    )
    op.add_column(
        "ibron",
        sa.Column(
            "ts_end",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'9999-12-31 23:59:59.999999+00'"),
        ),
    )

    op.add_column(
        "oe_struct_rolt",
        sa.Column(
            "ts_start",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'2023-01-01'"),
        ),
    )
    op.add_column(
        "oe_struct_rolt",
        sa.Column(
            "ts_end",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'9999-12-31 23:59:59.999999+00'"),
        ),
    )

    op.add_column(
        "rge",
        sa.Column(
            "ts_start",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'2023-01-01'"),
        ),
    )
    op.add_column(
        "rge",
        sa.Column(
            "ts_end",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'9999-12-31 23:59:59.999999+00'"),
        ),
    )

    op.add_column(
        "gst_gstt",
        sa.Column(
            "ts_start",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'2023-01-01'"),
        ),
    )
    op.add_column(
        "gst_gstt",
        sa.Column(
            "ts_end",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'9999-12-31 23:59:59.999999+00'"),
        ),
    )

    op.add_column(
        "evtp_oe_com_type",
        sa.Column(
            "ts_start",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'2023-01-01'"),
        ),
    )
    op.add_column(
        "evtp_oe_com_type",
        sa.Column(
            "ts_end",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'9999-12-31 23:59:59.999999+00'"),
        ),
    )

    op.add_column(
        "gg_struct",
        sa.Column(
            "ts_start",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'2023-01-01'"),
        ),
    )
    op.add_column(
        "gg_struct",
        sa.Column(
            "ts_end",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'9999-12-31 23:59:59.999999+00'"),
        ),
    )

    op.add_column(
        "oe_struct",
        sa.Column(
            "ts_start",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'2023-01-01'"),
        ),
    )
    op.add_column(
        "oe_struct",
        sa.Column(
            "ts_end",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'9999-12-31 23:59:59.999999+00'"),
        ),
    )

    op.drop_column("gg_struct", "ind_verplicht")
    op.drop_column("gg_struct", "ind_identificerend")

    op.drop_column("gst_gg_rge", "ind_expl")

    op.add_column(
        "gst_gg_rge",
        sa.Column(
            "ts_start",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'2023-01-01'"),
        ),
    )
    op.add_column(
        "gst_gg_rge",
        sa.Column(
            "ts_end",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("'9999-12-31 23:59:59.999999+00'"),
        ),
    )


# Define the downgrade operation (if needed)
def downgrade():
    # Step 6 (Reverse)
    op.drop_column("evtp_gst", "ts_end")
    op.drop_column("evtp_gst", "ts_start")

    op.drop_column("gg", "ts_end")
    op.drop_column("gg", "ts_start")

    op.drop_column("gst", "ts_end")
    op.drop_column("gst", "ts_start")

    op.drop_column("gst_type", "ts_end")
    op.drop_column("gst_type", "ts_start")

    op.drop_column("oe", "ts_end")
    op.drop_column("oe", "ts_start")

    op.drop_column("oe_type", "ts_end")
    op.drop_column("oe_type", "ts_start")

    op.drop_column("oe_com_type", "ts_end")
    op.drop_column("oe_com_type", "ts_start")

    op.drop_column("ibron", "ts_end")
    op.drop_column("ibron", "ts_start")

    op.drop_column("oe_struct_rolt", "ts_end")
    op.drop_column("oe_struct_rolt", "ts_start")

    op.drop_column("rge", "ts_end")
    op.drop_column("rge", "ts_start")

    op.drop_column("gst_gstt", "ts_end")
    op.drop_column("gst_gstt", "ts_start")

    op.drop_column("evtp_oe_com_type", "ts_end")
    op.drop_column("evtp_oe_com_type", "ts_start")

    op.drop_column("gg_struct", "ts_end")
    op.drop_column("gg_struct", "ts_start")

    op.drop_column("oe_struct", "ts_end")
    op.drop_column("oe_struct", "ts_start")

    op.drop_column("gst_gg_rge", "ts_end")
    op.drop_column("gst_gg_rge", "ts_start")

    # Step 5 (Reverse)
    # Add back the old columns
    op.add_column("evtp", sa.Column("evtp_upc_temp", sa.String(), nullable=True))  # Adjust the data type accordingly
    op.add_column("gst", sa.Column("gst_upc_temp", sa.String(), nullable=True))  # Adjust the data type accordingly

    # Copy data from the temporary columns to the old columns
    op.execute("""UPDATE evtp SET evtp_upc_temp = CAST(evtp_upc AS VARCHAR)""")
    op.execute("""UPDATE gst SET gst_upc_temp = CAST(gst_upc AS VARCHAR)""")

    # Drop the old columns
    op.drop_column("evtp", "evtp_upc")
    op.drop_column("gst", "gst_upc")

    # Rename the new columns back to the original names
    op.alter_column("evtp", "evtp_upc_temp", new_column_name="evtp_upc")
    op.alter_column("gst", "gst_upc_temp", new_column_name="gst_upc")

    # Step 4 (Reverse)
    op.add_column("evtp", sa.Column("evtp_nm", sa.String(), nullable=True))
    op.add_column("evtp", sa.Column("omschrijving", sa.String(), nullable=True))
    op.add_column("evtp", sa.Column("user_nm", sa.String(), nullable=True))
    op.add_column("evtp", sa.Column("notitie", sa.String(), nullable=True))
    op.add_column("evtp", sa.Column("evtp_cd_sup", sa.String(), nullable=True))
    op.add_column("evtp", sa.Column("srt_event", sa.String(), nullable=True))
    op.add_column("evtp", sa.Column("oe_best", sa.String(), nullable=True))
    op.add_column("evtp", sa.Column("aanleiding", sa.String(), nullable=True))
    op.add_column("evtp", sa.Column("gebr_dl", sa.String(), nullable=True))
    op.add_column("evtp", sa.Column("ind_pilot", sa.String(), nullable=True))
    op.add_column("evtp", sa.Column("sort_key", sa.String(), nullable=True))
    op.add_column("evtp", sa.Column("gg_cd", sa.Integer(), nullable=True))
    op.add_column("evtp", sa.Column("lidw_soort_besluit", sa.String(), nullable=True))
    op.add_column("evtp", sa.Column("soort_besluit", sa.String(), nullable=True))
    op.add_column("evtp", sa.Column("id_publicatiestatus", sa.Integer(), nullable=True))
    op.add_column("evtp", sa.Column("ts_mut", sa.DateTime(), nullable=True))

    # Step 3 (Reverse)
    op.execute(
        """
        UPDATE evtp_version
        SET id_publicatiestatus = CASE
            WHEN id_publicatiestatus = 1 THEN 1
            WHEN id_publicatiestatus = 2 THEN 1
            WHEN id_publicatiestatus = 3 THEN 2
            WHEN id_publicatiestatus = 4 THEN 2
            WHEN id_publicatiestatus = 5 THEN 3
            WHEN id_publicatiestatus = 6 THEN 4
            ELSE id_publicatiestatus
        END;
    """
    )

    # Step 2 (Reverse)
    op.execute("DELETE FROM evtp_version WHERE versie_nr = 1")

    # Step 1 (Reverse)
    op.drop_constraint("evpt_oe_fk", "evtp_version", type_="foreignkey")
    op.drop_constraint("evpt_evptsup_fk", "evtp_version", type_="foreignkey")

    op.drop_index("idx_18001_version_evtp_fk", table_name="evtp_version")
    op.drop_index("idx_17910_version_oe_fk", table_name="evtp_version")
