from dataclasses import dataclass
from enum import Enum
from typing import Dict, Type

import app.models as models
import app.schemas as schemas
from app.database.database import Base

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
    omg = "omg"
    gg = "gg"
    gg_koepel = "gg-koepel"
    gg_struct = "gg-struct"
    gg_evtp_sort = "gg-evtp-sort"
    gst = "gst"
    rge = "rge"
    oe_koepel_oe = "oe-koepel-oe"
    oe_koepel = "oe-koepel"
    ibron = "ibron"
    gst_gg = "gst-gg"
    gst_rge = "gst-rge"
    gst_type = "gst-type"
    gst_gstt = "gst-gstt"
    bestand_acc = "bestand-acc"
    ond = "ond"


@dataclass
class ResourceTableMapping:
    mapping: Dict[str, Type[Base]]

    def get_model(self, resource: str):
        return self.mapping[resource]

    def get_table_name(self, resource: TableResource) -> str:
        return self.mapping[resource].__tablename__


# Create the mapping
MAPPING_RESOURCE_TO_TABLE = ResourceTableMapping(
    {
        TableResource.evtp_version: models.evtp.EvtpVersion,
        TableResource.evtp_acc: models.evtp_acc.EvtpAcc,
        TableResource.evtp_gst: models.evtp.EvtpGst,
        TableResource.evtp_oe_com_type: models.evtp.EvtpOeComType,
        TableResource.oe: models.oe.Oe,
        TableResource.oe_com_type: models.oe.OeComType,
        TableResource.omg: models.evtp.Omg,
        TableResource.gg: models.gg.Gg,
        TableResource.gg_koepel: models.gg.Gg,
        TableResource.gg_struct: models.gg.GgStruct,
        TableResource.gg_evtp_sort: models.gg.GgEvtpSort,
        TableResource.gst: models.gst.Gst,
        TableResource.rge: models.rge.Rge,
        TableResource.oe_koepel_oe: models.oe.OeKoepelOe,
        TableResource.oe_koepel: models.oe.OeKoepel,
        TableResource.ibron: models.ibron.Ibron,
        TableResource.gst_gg: models.gst.GstGg,
        TableResource.gst_rge: models.gst.GstRge,
        TableResource.gst_type: models.gst.GstType,
        TableResource.gst_gstt: models.gst.GstGstt,
        TableResource.bestand_acc: models.evtp_acc.BestandAcc,
        TableResource.ond: models.ond.Ond,
        TableResource.evtp_ond: models.ond.EvtpOnd,
    }
)


@dataclass
class Status:
    code: int
    description: str


class MappingPublicatiestatus(Enum):
    NEW = Status(1, "Nieuw")
    READY = Status(2, "Gereed voor controle")
    PUBLISHED = Status(3, "Gepubliceerd")
    ARCHIVED = Status(4, "Gearchiveerd")

    @property
    def code(self) -> int:
        return self.value.code

    @property
    def description(self):
        return self.value.description


EXCEPTIONS_REQUIRED_FIELDS: Dict[str, list] = {
    TableResource.evtp_version.value: ["oe_best"],
    TableResource.evtp_gst.value: [],
    TableResource.evtp_acc.value: [],
    TableResource.evtp_oe_com_type.value: [],
    TableResource.omg.value: [],
    TableResource.oe.value: ["naam_officieel"],
    TableResource.oe_com_type.value: [],
    TableResource.gg.value: [],
    TableResource.gg_struct.value: [],
    TableResource.gg_evtp_sort.value: [],
    TableResource.gst.value: [],
    TableResource.rge.value: ["re_link"],
    TableResource.oe_koepel_oe.value: [],
    TableResource.oe_koepel.value: [],
    TableResource.ibron.value: [],
    TableResource.gst_gg.value: [],
    TableResource.gst_type.value: [],
    TableResource.gst_gstt.value: [],
    TableResource.bestand_acc.value: [],
    TableResource.ond.value: [],
    TableResource.evtp_ond.value: [],
}

URL_PER_RESOURCE: Dict[str, list] = {
    TableResource.evtp_version: ["overige_informatie_link", "uri"],
    TableResource.evtp_gst: [],
    TableResource.evtp_acc: [],
    TableResource.evtp_oe_com_type: ["link"],
    TableResource.omg: ["link"],
    TableResource.oe: ["internet_domein"],
    TableResource.oe_com_type: [],
    TableResource.gg: [],
    TableResource.gg_struct: [],
    TableResource.gg_evtp_sort: [],
    TableResource.gst: ["ext_lnk_aut"],
    TableResource.rge: ["re_link"],
    TableResource.oe_koepel_oe: [],
    TableResource.oe_koepel: [],
    TableResource.ibron: ["link"],
    TableResource.gst_gg: [],
    TableResource.gst_type: [],
    TableResource.gst_gstt: [],
    TableResource.bestand_acc: [],
    TableResource.ond: [],
    TableResource.evtp_ond: [],
}


@dataclass
class TableToResourceMapping:
    resource: TableResource
    description_key: str
    primary_key: str
    foreign_key_mapping: Dict[str, str]
    input_schema: Type | None


MAPPING_TABLE_TO_RESOURCE: Dict[str, TableToResourceMapping] = {
    models.oe.Oe.__tablename__: TableToResourceMapping(
        resource=TableResource.oe,
        description_key=models.oe.Oe.naam_officieel.name,
        primary_key=models.oe.Oe.oe_cd.name,
        foreign_key_mapping={},
        input_schema=schemas.oe.OeIn,
    ),
    models.gg.Gg.__tablename__: TableToResourceMapping(
        resource=TableResource.gg,
        description_key=models.gg.Gg.omschrijving.name,
        primary_key=models.gg.Gg.gg_cd.name,
        foreign_key_mapping={},
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
            "omg_cd": "entity_omg",
        },
        input_schema=schemas.evtp_version.EvtpVersionIn,
    ),
    models.oe.OeKoepel.__tablename__: TableToResourceMapping(
        resource=TableResource.oe_koepel,
        description_key=models.evtp.Omg.titel.name,
        primary_key=models.oe.OeKoepel.oe_koepel_cd.name,
        foreign_key_mapping={},
        input_schema=schemas.oe_koepel.OeKoepelIn,
    ),
    models.oe.OeKoepelOe.__tablename__: TableToResourceMapping(
        resource=TableResource.oe_koepel_oe,
        description_key="",
        primary_key=models.oe.OeKoepelOe.oe_koepel_oe_cd.name,
        foreign_key_mapping={
            "oe_cd": "child_entity",
            "oe_koepel_cd": "parent_entity",
        },
        input_schema=schemas.oe_koepel_oe.OeKoepelOeIn,
    ),
    models.ibron.Ibron.__tablename__: TableToResourceMapping(
        resource=TableResource.ibron,
        description_key=models.ibron.Ibron.titel.name,
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
    models.evtp.Omg.__tablename__: TableToResourceMapping(
        resource=TableResource.omg,
        description_key="titel",
        primary_key=models.evtp.Omg.omg_cd.name,
        foreign_key_mapping={
            "oe_cd": "entity_oe",
        },
        input_schema=schemas.omg.OmgIn,
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
