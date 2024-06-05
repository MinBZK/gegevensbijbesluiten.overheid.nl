from fastapi import APIRouter

from app.api.endpoints import _generic_tables, config, evtp_acc, evtp_version, table

router = APIRouter()

# ----------------------------------------------- Config -----------------------------------------------
router.include_router(
    config.router,
    prefix="/config",
    tags=["Configuratie"],
)

# ----------------------------------------------- Tables -----------------------------------------------

router.include_router(
    _generic_tables.gst_type_router,
    prefix="/gst-type",
    tags=["Gegevensstroomtype"],
)


router.include_router(
    _generic_tables.gst_gstt_router,
    prefix="/gst-gstt",
    tags=["Gegevensstroom Gegevensstroomtype"],
)

router.include_router(
    _generic_tables.gst_gg_router,
    prefix="/gst-gg",
    tags=["Gegevensstroom Gegevensgroep"],
)

router.include_router(
    _generic_tables.gst_rge_router,
    prefix="/gst-rge",
    tags=["Gegevensstroom Regelingelement"],
)

router.include_router(
    _generic_tables.evtp_gst_router,
    prefix="/evtp-gst",
    tags=["Besluit Gegevensstroom"],
)

router.include_router(
    evtp_acc.evtp_acc_router,
    prefix="/evtp-acc",
    tags=["Besluit Accordering"],
)

router.include_router(
    _generic_tables.gg_evtp_sort,
    prefix="/gg-evtp-sort",
    tags=["Gegevensgroep sortering per besluit"],
)

router.include_router(
    _generic_tables.oe_router,
    prefix="/oe",
    tags=["Organisatie"],
)

router.include_router(
    _generic_tables.oe_struct_router,
    prefix="/oe-struct",
    tags=["Organisatie structuur"],
)

router.include_router(
    _generic_tables.gg_router,
    prefix="/gg",
    tags=["Gegevensgroep"],
)

router.include_router(
    _generic_tables.gg_koepel_router,
    prefix="/gg-koepel",
    tags=["Gegevensgroep"],
)

router.include_router(
    _generic_tables.gg_struct,
    prefix="/gg-struct",
    tags=["Gegevensgroepstructuur"],
)

router.include_router(
    _generic_tables.gst_router,
    prefix="/gst",
    tags=["Gegevensstroom"],
)

router.include_router(
    evtp_version.router,
    prefix="/evtp-version",
    tags=["Besluit"],
)

router.include_router(
    _generic_tables.rge_router,
    prefix="/rge",
    tags=["Regelingelement"],
)

router.include_router(
    _generic_tables.ibron_router,
    prefix="/ibron",
    tags=["Informatiebron"],
)

router.include_router(
    table.router,
    prefix="/table",
    tags=["Tabel"],
)

router.include_router(
    _generic_tables.oe_com_type_router,
    prefix="/oe-com-type",
    tags=["Organisatie communicatie kanaal"],
)

router.include_router(
    _generic_tables.evtp_oe_com_type_router,
    prefix="/evtp-oe-com-type",
    tags=["Besluit organisatie communicatie kanalen"],
)

router.include_router(
    _generic_tables.ond_router,
    prefix="/ond",
    tags=["Onderwerp"],
)

router.include_router(
    _generic_tables.evtp_ond_router,
    prefix="/evtp-ond",
    tags=["Besluit onderwerp"],
)
