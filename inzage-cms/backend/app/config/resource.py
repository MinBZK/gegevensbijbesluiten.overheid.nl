from dataclasses import dataclass
from enum import Enum
from typing import Dict, Type

import app.models as models
import app.schemas as schemas

PATH_MNT = "../mnt/accorderingen"
LIMIT_RESULTS_QUERY = 100


class TableResource(str, Enum):
    evtp_version = "evtp-version"
    evtp_gst = "evtp-gst"
    evtp_acc = "evtp-acc"
    evtp_ond = "evtp-ond"
    evtp_oe_com_type = "evtp-oe-com-type"
    oe = "oe"
    oe_com_type = "oe-com-type"
    gg = "gg"
    gg_koepel = "gg-koepel"
    gg_struct = "gg-struct"
    gg_evtp_sort = "gg-evtp-sort"
    gst = "gst"
    rge = "rge"
    oe_struct = "oe-struct"
    ibron = "ibron"
    gst_gg = "gst-gg"
    gst_rge = "gst-rge"
    gst_type = "gst-type"
    gst_gstt = "gst-gstt"
    bestand_acc = "bestand-acc"
    ond = "ond"


MAPPING_RESOURCE_TO_TABLE = {
    TableResource.evtp_version.value: models.evtp.EvtpVersion.__tablename__,
    TableResource.evtp_acc.value: models.evtp_acc.EvtpAcc.__tablename__,
    TableResource.evtp_gst.value: models.evtp.EvtpGst.__tablename__,
    TableResource.evtp_oe_com_type.value: models.evtp.EvtpOeComType.__tablename__,
    TableResource.oe.value: models.oe.Oe.__tablename__,
    TableResource.oe_com_type.value: models.oe.OeComType.__tablename__,
    TableResource.gg.value: models.gg.Gg.__tablename__,
    TableResource.gg_koepel.value: models.gg.Gg.__tablename__,
    TableResource.gg_struct.value: models.gg.GgStruct.__tablename__,
    TableResource.gg_evtp_sort.value: models.gg.GgEvtpSort.__tablename__,
    TableResource.gst.value: models.gst.Gst.__tablename__,
    TableResource.rge.value: models.rge.Rge.__tablename__,
    TableResource.oe_struct.value: models.oe.OeStruct.__tablename__,
    TableResource.ibron.value: models.ibron.Ibron.__tablename__,
    TableResource.gst_gg.value: models.gst.GstGg.__tablename__,
    TableResource.gst_rge.value: models.gst.GstRge.__tablename__,
    TableResource.gst_type.value: models.gst.GstType.__tablename__,
    TableResource.gst_gstt.value: models.gst.GstGstt.__tablename__,
    TableResource.bestand_acc.value: models.evtp_acc.BestandAcc.__tablename__,
    TableResource.ond.value: models.ond.Ond.__tablename__,
    TableResource.evtp_ond.value: models.ond.EvtpOnd.__tablename__,
}


class MappingPublicatiestatus(tuple, Enum):
    NEW = (1, "Nieuw")
    READY = (2, "Gereed voor controle")
    PUBLISHED = (3, "Gepubliceerd")
    ARCHIVED = (4, "Gearchiveerd")


EXCEPTIONS_REQUIRED_FIELDS = {
    TableResource.evtp_version.value: ["oe_best", "omschrijving"],
    TableResource.evtp_gst.value: [],
    TableResource.evtp_acc.value: [],
    TableResource.evtp_oe_com_type.value: [],
    TableResource.oe.value: ["naam_officieel"],
    TableResource.oe_com_type.value: [],
    TableResource.gg.value: ["omschrijving_uitgebreid", "omschrijving"],
    TableResource.gg_struct.value: [],
    TableResource.gg_evtp_sort.value: [],
    TableResource.gst.value: [],
    TableResource.rge.value: [],
    TableResource.oe_struct.value: [],
    TableResource.ibron.value: [],
    TableResource.gst_gg.value: [],
    TableResource.gst_type.value: ["gstt_oms"],
    TableResource.gst_gstt.value: [],
    TableResource.bestand_acc.value: [],
    TableResource.ond.value: [],
    TableResource.evtp_ond.value: [],
}


@dataclass
class TableToResourceMapping:
    resource: TableResource
    description_key: str
    primary_key: str
    foreign_key_mapping: Dict[str, str]
    input_schema: Type | None


MAPPING_TABLE_TO_RESOURCE = {
    models.oe.Oe.__tablename__: TableToResourceMapping(
        resource=TableResource.oe,
        description_key=models.oe.Oe.naam_officieel.name,
        primary_key=models.oe.Oe.oe_cd.name,
        foreign_key_mapping={
            "ibron_cd": "entity_ibron",
        },
        input_schema=schemas.oe.OeIn,
    ),
    models.gg.Gg.__tablename__: TableToResourceMapping(
        resource=TableResource.gg,
        description_key=models.gg.Gg.omschrijving.name,
        primary_key=models.gg.Gg.gg_cd.name,
        foreign_key_mapping={
            "ibron_cd": "entity_ibron",
        },
        input_schema=schemas.gg.GgIn,
    ),
    models.gg.GgStruct.__tablename__: TableToResourceMapping(
        resource=TableResource.gg_struct,
        description_key="",
        primary_key=models.gg.GgStruct.gg_struct_cd.name,
        foreign_key_mapping={
            "gg_cd_sub": "child_entity",
            "gg_cd_sup": "parent_entity",
        },
        input_schema=schemas.gg_struct.GgStructIn,
    ),
    models.gg.GgEvtpSort.__tablename__: TableToResourceMapping(
        resource=TableResource.gg_evtp_sort,
        description_key="",
        primary_key=models.gg.GgEvtpSort.gg_evtp_sort_cd.name,
        foreign_key_mapping={
            "gg_cd": "entity_gg",
            "evtp_cd": "entity_evtp_version",
        },
        input_schema=schemas.gg_evtp_sort.GgEvtpSortIn,
    ),
    models.rge.Rge.__tablename__: TableToResourceMapping(
        resource=TableResource.rge,
        description_key=models.rge.Rge.titel.name,
        primary_key=models.rge.Rge.rge_cd.name,
        foreign_key_mapping={},
        input_schema=schemas.rge.RgeIn,
    ),
    models.gst.Gst.__tablename__: TableToResourceMapping(
        resource=TableResource.gst,
        description_key=models.gst.Gst.omschrijving.name,
        primary_key=models.gst.Gst.gst_cd.name,
        foreign_key_mapping={
            "oe_best": "entity_oe_best",
            "oe_bron": "entity_oe_bron",
            "ibron_cd": "entity_ibron",
        },
        input_schema=schemas.gst.GstIn,
    ),
    models.gst.GstGg.__tablename__: TableToResourceMapping(
        resource=TableResource.gst_gg,
        description_key="",
        primary_key=models.gst.GstGg.gst_gg_cd.name,
        foreign_key_mapping={
            "gg_cd": "entity_gg",
            "gst_cd": "entity_gst",
        },
        input_schema=schemas.gst_gg.GstGgIn,
    ),
    models.gst.GstRge.__tablename__: TableToResourceMapping(
        resource=TableResource.gst_rge,
        description_key="",
        primary_key=models.gst.GstRge.gst_rge_cd.name,
        foreign_key_mapping={
            "gst_cd": "entity_gst",
            "rge_cd": "entity_rge",
        },
        input_schema=schemas.gst_rge.GstRgeIn,
    ),
    models.evtp.EvtpVersion.__tablename__: TableToResourceMapping(
        resource=TableResource.evtp_version,
        description_key=models.evtp.EvtpVersion.evtp_nm.name,
        primary_key=models.evtp.EvtpVersion.evtp_cd.name,
        foreign_key_mapping={
            "oe_best": "verantwoordelijke_oe",
            "evtp_cd_sup": "parent_evtp",
        },
        input_schema=schemas.evtp_version.EvtpVersionIn,
    ),
    models.oe.OeStruct.__tablename__: TableToResourceMapping(
        resource=TableResource.oe_struct,
        description_key="",
        primary_key=models.oe.OeStruct.oe_struct_cd.name,
        foreign_key_mapping={
            "oe_cd_sub": "child_entity",
            "oe_cd_sup": "parent_entity",
        },
        input_schema=schemas.oe_struct.OeStructIn,
    ),
    models.ibron.Ibron.__tablename__: TableToResourceMapping(
        resource=TableResource.ibron,
        description_key=models.ibron.Ibron.omschrijving.name,
        primary_key=models.ibron.Ibron.ibron_cd.name,
        foreign_key_mapping={"oe_cd": "entity_oe"},
        input_schema=schemas.ibron.IbronIn,
    ),
    models.evtp.EvtpGst.__tablename__: TableToResourceMapping(
        resource=TableResource.evtp_gst,
        description_key="",
        primary_key=models.evtp.EvtpGst.evtp_gst_cd.name,
        foreign_key_mapping={
            "evtp_cd": "entity_evtp_version",
            "gst_cd": "entity_gst",
        },
        input_schema=schemas.evtp_gst.EvtpGstIn,
    ),
    models.gst.GstType.__tablename__: TableToResourceMapping(
        resource=TableResource.gst_type,
        description_key=models.gst.GstType.gstt_naam.name,
        primary_key=models.gst.GstType.gstt_cd.name,
        foreign_key_mapping={},
        input_schema=schemas.gst_type.GstTypeIn,
    ),
    models.gst.GstGstt.__tablename__: TableToResourceMapping(
        resource=TableResource.gst_gstt,
        description_key="",
        primary_key=models.gst.GstGstt.gst_gstt_cd.name,
        foreign_key_mapping={
            "gstt_cd": "entity_gst_type",
            "gst_cd": "entity_gst_gstt",
        },
        input_schema=schemas.gst_gstt.GstGsttIn,
    ),
    models.evtp_acc.EvtpAcc.__tablename__: TableToResourceMapping(
        resource=TableResource.evtp_acc,
        description_key=models.evtp_acc.EvtpAcc.notitie.name,
        primary_key=models.evtp_acc.EvtpAcc.evtp_acc_cd.name,
        foreign_key_mapping={
            "evtp_cd": "entity_evtp_version",
            "oe_cd": "entity_oe",
        },
        input_schema=schemas.evtp_acc.EvtpAccIn,
    ),
    models.evtp_acc.BestandAcc.__tablename__: TableToResourceMapping(
        resource=TableResource.bestand_acc,
        description_key="",
        primary_key=models.evtp_acc.BestandAcc.bestand_acc_cd.name,
        foreign_key_mapping={},
        input_schema=None,
    ),
    models.evtp.EvtpOeComType.__tablename__: TableToResourceMapping(
        resource=TableResource.evtp_oe_com_type,
        description_key="",
        primary_key=models.evtp.EvtpOeComType.evtp_oe_com_type_cd.name,
        foreign_key_mapping={
            "evtp_cd": "entity_evtp_version_oe_com_type",
            "oe_com_type_cd": "entity_oe_com_type",
        },
        input_schema=schemas.evtp_oe_com_type.EvtpOeComTypeIn,
    ),
    models.oe.OeComType.__tablename__: TableToResourceMapping(
        resource=TableResource.oe_com_type,
        description_key=models.oe.OeComType.omschrijving.name,
        primary_key=models.oe.OeComType.oe_com_type_cd.name,
        foreign_key_mapping={},
        input_schema=schemas.oe_com_type.OeComTypeIn,
    ),
    models.ond.Ond.__tablename__: TableToResourceMapping(
        resource=TableResource.ond,
        description_key=models.ond.Ond.titel.name,
        primary_key=models.ond.Ond.ond_cd.name,
        foreign_key_mapping={},
        input_schema=schemas.ond.OndIn,
    ),
    models.ond.EvtpOnd.__tablename__: TableToResourceMapping(
        resource=TableResource.evtp_ond,
        description_key="",
        primary_key=models.ond.EvtpOnd.evtp_ond_cd.name,
        foreign_key_mapping={
            "evtp_cd": "entity_evtp_version",
            "ond_cd": "entity_ond",
        },
        input_schema=schemas.evtp_ond.EvtpOndIn,
    ),
}
