import app.models as models
from app.api.endpoints._default import (
    delete_attr,
    delete_relation_parent_child,
    generate_router,
    get_child_gg,
    get_child_gg_filtered,
    get_parent_gg,
)
from app.config.resource import TableResource

# Generate endpoints for all models that fits the generic table pattern
evtp_gst_router = generate_router(
    model_name=TableResource.evtp_gst.name, base_model=models.evtp.EvtpGst, additional_routes=[delete_attr]
)
evtp_oe_com_type_router = generate_router(
    model_name=TableResource.evtp_oe_com_type.name, base_model=models.evtp.EvtpOeComType
)
evtp_ond_router = generate_router(model_name=TableResource.evtp_ond.name, base_model=models.ond.EvtpOnd)
gg_struct = generate_router(
    model_name=TableResource.gg_struct.name,
    base_model=models.gg.GgStruct,
    additional_routes=[delete_relation_parent_child],
)

gg_router = generate_router(
    model_name=TableResource.gg.name,
    base_model=models.gg.Gg,
    filter_by_default={"koepel": False},
    additional_routes=[get_parent_gg, get_child_gg_filtered],
)
gg_koepel_router = generate_router(
    model_name=TableResource.gg.name,
    base_model=models.gg.Gg,
    filter_by_default={"koepel": True},
    additional_routes=[get_child_gg],
)
gst_gg_router = generate_router(model_name=TableResource.gst_gg.name, base_model=models.gst.GstGg)
gst_gstt_router = generate_router(model_name=TableResource.gst_gstt.name, base_model=models.gst.GstGstt)
gst_rge_router = generate_router(model_name=TableResource.gst_rge.name, base_model=models.gst.GstRge)
gst_type_router = generate_router(model_name=TableResource.gst_type.name, base_model=models.gst.GstType)
gst_router = generate_router(model_name=TableResource.gst.name, base_model=models.gst.Gst)
ibron_router = generate_router(model_name=TableResource.ibron.name, base_model=models.ibron.Ibron)
oe_com_type_router = generate_router(model_name=TableResource.oe_com_type.name, base_model=models.oe.OeComType)
omg_router = generate_router(model_name=TableResource.omg.name, base_model=models.evtp.Omg)
oe_koepel_oe_router = generate_router(
    model_name=TableResource.oe_koepel_oe.name,
    base_model=models.oe.OeKoepelOe,
    additional_routes=[delete_relation_parent_child],
)
oe_koepel_router = generate_router(model_name=TableResource.oe_koepel.name, base_model=models.oe.OeKoepel)

oe_router = generate_router(model_name=TableResource.oe.name, base_model=models.oe.Oe)
rge_router = generate_router(model_name=TableResource.rge.name, base_model=models.rge.Rge)
ond_router = generate_router(model_name=TableResource.ond.name, base_model=models.ond.Ond)
gg_evtp_sort = generate_router(model_name=TableResource.gg_evtp_sort.name, base_model=models.gg.GgEvtpSort)
