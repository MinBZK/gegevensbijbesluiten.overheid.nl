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
    # dependencies=[Depends(dependencies.get_current_gebruiker)],
)


router.include_router(
    _generic_tables.gst_gstt_router,
    prefix="/gst-gstt",
    tags=["Gegevensstroom Gegevensstroomtype"],
    # dependencies=[Depends(dependencies.get_current_gebruiker)],
)

router.include_router(
    _generic_tables.gst_gg_router,
    prefix="/gst-gg",
    tags=["Gegevensstroom Gegevensgroep"],
    # dependencies=[Depends(dependencies.get_current_gebruiker)],
)

router.include_router(
    _generic_tables.gst_rge_router,
    prefix="/gst-rge",
    tags=["Gegevensstroom Regelingelement"],
    # dependencies=[Depends(dependencies.get_current_gebruiker)],
)

router.include_router(
    _generic_tables.evtp_gst_router,
    prefix="/evtp-gst",
    tags=["Besluit Gegevensstroom"],
    # dependencies=[Depends(dependencies.get_current_gebruiker)],
)

router.include_router(
    evtp_acc.evtp_acc_router,
    prefix="/evtp-acc",
    tags=["Besluit Accordering"],
    # dependencies=[Depends(dependencies.get_current_gebruiker)],
)

router.include_router(
    _generic_tables.gg_evtp_sort,
    prefix="/gg-evtp-sort",
    tags=["Gegevensgroep sortering per besluit"],
    # dependencies=[Depends(dependencies.get_current_gebruiker)],
)

router.include_router(
    _generic_tables.oe_router,
    prefix="/oe",
    tags=["Organisatie"],
    # dependencies=[Depends(dependencies.get_current_gebruiker)],
)

router.include_router(
    _generic_tables.oe_struct_router,
    prefix="/oe-struct",
    tags=["Organisatie structuur"],
    # dependencies=[Depends(dependencies.get_current_gebruiker)],
)

router.include_router(
    _generic_tables.gg_router,
    prefix="/gg",
    tags=["Gegevensgroep"],
    # dependencies=[Depends(dependencies.get_current_gebruiker)],
)

router.include_router(
    _generic_tables.gg_koepel_router,
    prefix="/gg-koepel",
    tags=["Gegevensgroep"],
    # dependencies=[Depends(dependencies.get_current_gebruiker)],
)

router.include_router(
    _generic_tables.gg_struct,
    prefix="/gg-struct",
    tags=["Gegevensgroepstructuur"],
    # dependencies=[Depends(dependencies.get_current_gebruiker)],
)

router.include_router(
    _generic_tables.gst_router,
    prefix="/gst",
    tags=["Gegevensstroom"],
    # dependencies=[Depends(dependencies.get_current_gebruiker)],
)

router.include_router(
    evtp_version.router,
    prefix="/evtp-version",
    tags=["Besluit"],
    # dependencies=[Depends(dependencies.get_current_gebruiker)],
)

router.include_router(
    _generic_tables.rge_router,
    prefix="/rge",
    tags=["Regelingelement"],
    # dependencies=[Depends(dependencies.get_current_gebruiker)],
)

router.include_router(
    _generic_tables.ibron_router,
    prefix="/ibron",
    tags=["Informatiebron"],
    # dependencies=[Depends(dependencies.get_current_gebruiker)],
)

router.include_router(
    table.router,
    prefix="/table",
    tags=["Tabel"],
    # dependencies=[Depends(dependencies.get_current_gebruiker)],
)

router.include_router(
    _generic_tables.oe_com_type_router,
    prefix="/oe-com-type",
    tags=["Organisatie communicatie kanaal"],
    # dependencies=[Depends(dependencies.get_current_gebruiker)],
)

router.include_router(
    _generic_tables.evtp_oe_com_type_router,
    prefix="/evtp-oe-com-type",
    tags=["Besluit organisatie communicatie kanalen"],
    # dependencies=[Depends(dependencies.get_current_gebruiker)],
)

router.include_router(
    _generic_tables.ond_router,
    prefix="/ond",
    tags=["Onderwerp"],
    # dependencies=[Depends(dependencies.get_current_gebruiker)],
)

router.include_router(
    _generic_tables.evtp_ond_router,
    prefix="/evtp-ond",
    tags=["Besluit onderwerp"],
    # dependencies=[Depends(dependencies.get_current_gebruiker)],
)
