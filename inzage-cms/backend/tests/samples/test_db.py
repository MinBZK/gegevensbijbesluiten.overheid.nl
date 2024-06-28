import logging
from dataclasses import dataclass
from typing import NamedTuple

import app.models as models
import app.schemas as schemas
import pytest
from app.config.resource import TableResource
from sqlalchemy import select

logger = logging.getLogger(__name__)


class PrimaryKeys(NamedTuple):
    database_pk: int
    post_pk: int | None


@dataclass
class ResourcePks:
    evtp_version: PrimaryKeys
    evtp_acc: PrimaryKeys
    evtp_gst: PrimaryKeys
    evtp_oe_com_type: PrimaryKeys
    gg: PrimaryKeys
    gg_struct: PrimaryKeys
    gst_gg: PrimaryKeys
    gst_type: PrimaryKeys
    gst_gstt: PrimaryKeys
    gst: PrimaryKeys
    ibron: PrimaryKeys
    oe_com_type: PrimaryKeys
    oe_koepel: PrimaryKeys
    oe_koepel_oe: PrimaryKeys
    oe: PrimaryKeys
    rge: PrimaryKeys
    ond: PrimaryKeys
    evtp_ond: PrimaryKeys
    gg_evtp_sort: PrimaryKeys


@dataclass
class ResourcePayloads:
    evtp_version: schemas.evtp_version.EvtpNewVersionIn
    evtp_acc: schemas.evtp_acc.EvtpAccIn
    evtp_gst: schemas.evtp_gst.EvtpGstIn
    evtp_oe_com_type: schemas.evtp_oe_com_type.EvtpOeComTypeIn
    gg: schemas.gg.GgIn
    gg_struct: schemas.gg_struct.GgStructIn
    gst_gg: schemas.gst_gg.GstGgIn
    gst_type: schemas.gst_type.GstTypeIn
    gst_gstt: schemas.gst_gstt.GstGsttIn
    gst: schemas.gst.GstIn
    ibron: schemas.ibron.IbronIn
    oe_com_type: schemas.oe_com_type.OeComTypeIn
    oe_koepel_oe: schemas.oe_koepel_oe.OeKoepelOeIn
    oe_koepel: schemas.oe_koepel.OeKoepelIn
    oe: schemas.oe.OeIn
    rge: schemas.rge.RgeIn
    ond: schemas.ond.OndIn
    evtp_ond: schemas.evtp_ond.EvtpOndIn
    gg_evtp_sort: schemas.gg_evtp_sort.GgEvtpSortIn


def populate_payloads(resource_pks: ResourcePks, resource_payloads: ResourcePayloads):
    resource_payloads.evtp_version.oe_best = resource_pks.oe.database_pk
    resource_payloads.evtp_version.evtp_cd_sup = resource_pks.evtp_version.database_pk
    resource_payloads.evtp_acc.evtp_cd = resource_pks.evtp_version.database_pk
    resource_payloads.evtp_acc.oe_cd = resource_pks.oe.database_pk
    resource_payloads.evtp_gst.evtp_cd = resource_pks.evtp_version.database_pk
    resource_payloads.evtp_gst.gst_cd = resource_pks.gst.database_pk
    resource_payloads.evtp_oe_com_type.evtp_cd = resource_pks.evtp_version.database_pk
    resource_payloads.evtp_oe_com_type.oe_com_type_cd = resource_pks.oe_com_type.database_pk
    resource_payloads.gg_struct.gg_cd_sub = resource_pks.gg.database_pk
    resource_payloads.gg_struct.gg_cd_sup = resource_pks.gg.database_pk
    resource_payloads.gst_gg.gg_cd = resource_pks.gg.database_pk
    resource_payloads.gst_gg.gst_cd = resource_pks.gst.database_pk
    resource_payloads.gst.oe_best = resource_pks.oe.database_pk
    resource_payloads.gst.oe_bron = resource_pks.oe.database_pk
    resource_payloads.gst.ibron_cd = resource_pks.ibron.database_pk
    resource_payloads.gst_gstt.gst_cd = resource_pks.gst.database_pk
    resource_payloads.gst_gstt.gstt_cd = resource_pks.gst_gstt.database_pk
    resource_payloads.ibron.oe_cd = resource_pks.oe.database_pk
    resource_payloads.oe_koepel_oe.oe_cd = resource_pks.oe.database_pk
    resource_payloads.oe_koepel_oe.oe_koepel_cd = resource_pks.oe_koepel.database_pk
    resource_payloads.oe.ibron_cd = resource_pks.ibron.database_pk
    resource_payloads.evtp_ond.evtp_cd = resource_pks.evtp_version.database_pk
    resource_payloads.evtp_ond.ond_cd = resource_pks.ond.database_pk
    resource_payloads.gg_evtp_sort.gg_cd = resource_pks.gg.database_pk
    resource_payloads.gg_evtp_sort.evtp_cd = resource_pks.evtp_version.database_pk
    return resource_payloads


@pytest.fixture()
def resource_pks(db):
    pks = ResourcePks(
        evtp_version=PrimaryKeys(db.scalars(select(models.evtp.Evtp.evtp_cd)).first(), None),
        evtp_acc=PrimaryKeys(db.scalars(select(models.evtp_acc.EvtpAcc.evtp_acc_cd)).first(), None),
        evtp_gst=PrimaryKeys(db.scalars(select(models.evtp.EvtpGst.evtp_gst_cd)).first(), None),
        evtp_oe_com_type=PrimaryKeys(db.scalars(select(models.evtp.EvtpOeComType.evtp_cd)).first(), None),
        gg=PrimaryKeys(db.scalars(select(models.gg.Gg.gg_cd)).first(), None),
        gg_struct=PrimaryKeys(db.scalars(select(models.gg.GgStruct.gg_cd_sub)).first(), None),
        gst_gg=PrimaryKeys(db.scalars(select(models.gst.GstGg.gst_gg_cd)).first(), None),
        gst_type=PrimaryKeys(db.scalars(select(models.gst.GstType.gstt_cd)).first(), None),
        gst_gstt=PrimaryKeys(db.scalars(select(models.gst.GstGstt.gst_gstt_cd)).first(), None),
        gst=PrimaryKeys(db.scalars(select(models.gst.Gst.gst_cd)).first(), None),
        ibron=PrimaryKeys(db.scalars(select(models.ibron.Ibron.ibron_cd)).first(), None),
        oe_com_type=PrimaryKeys(db.scalars(select(models.oe.OeComType.oe_com_type_cd)).first(), None),
        oe_koepel_oe=PrimaryKeys(db.scalars(select(models.oe.OeKoepelOe.oe_koepel_oe_cd)).first(), None),
        oe_koepel=PrimaryKeys(db.scalars(select(models.oe.OeKoepel.oe_koepel_cd)).first(), None),
        oe=PrimaryKeys(db.scalars(select(models.oe.Oe.oe_cd)).first(), None),
        rge=PrimaryKeys(db.scalars(select(models.rge.Rge.rge_cd)).first(), None),
        ond=PrimaryKeys(db.scalars(select(models.ond.Ond.ond_cd)).first(), None),
        evtp_ond=PrimaryKeys(db.scalars(select(models.ond.EvtpOnd.evtp_ond_cd)).first(), None),
        gg_evtp_sort=PrimaryKeys(db.scalars(select(models.gg.GgEvtpSort.gg_evtp_sort_cd)).first(), None),
    )
    return pks


@pytest.fixture()
def resource_payloads(resource_pks):
    standard_text = "PyTest"
    standard_value = 1
    payloads = ResourcePayloads(
        evtp_version=schemas.evtp_version.EvtpNewVersionIn(
            aanleiding=standard_text,
            evtp_cd_sup=standard_value,
            evtp_nm=standard_text,
            gebr_dl=standard_text,
            notitie=standard_text,
            oe_best=standard_value,
            omschrijving=standard_text,
            uri=standard_text,
            soort_besluit=standard_text,
            lidw_soort_besluit=standard_text,
            versie_nr=standard_value,
        ),
        gg=schemas.gg.GgIn(
            omschrijving=standard_text, omschrijving_uitgebreid=standard_text, notitie=standard_text, koepel=True
        ),
        evtp_acc=schemas.evtp_acc.EvtpAccIn(
            evtp_cd=standard_value,
            oe_cd=standard_value,
            notitie=standard_text,
            volg_nr=standard_value,
        ),
        evtp_gst=schemas.evtp_gst.EvtpGstIn(
            conditie=standard_text,
            evtp_cd=standard_value,
            versie_nr=standard_value,
            gst_cd=standard_value,
            notitie=standard_text,
            sort_key=standard_value,
        ),
        evtp_oe_com_type=schemas.evtp_oe_com_type.EvtpOeComTypeIn(
            evtp_cd=standard_value,
            versie_nr=standard_value,
            oe_com_type_cd=standard_value,
            link=standard_text,
        ),
        gg_struct=schemas.gg_struct.GgStructIn(
            gg_cd_sub=standard_value,
            gg_cd_sup=standard_value,
            notitie=standard_text,
        ),
        gst_gg=schemas.gst_gg.GstGgIn(
            gg_cd=standard_value,
            gst_cd=standard_value,
            versie_nr=standard_value,
            notitie=standard_text,
            sort_key=standard_value,
        ),
        gst_type=schemas.gst_type.GstTypeIn(
            gstt_naam=standard_text,
            gstt_oms=standard_text,
            gstt_pp=standard_text,
        ),
        gst_gstt=schemas.gst_gstt.GstGsttIn(
            gst_cd=standard_value,
            versie_nr=standard_value,
            gstt_cd=standard_value,
        ),
        gst=schemas.gst.GstIn(
            ext_lnk_aut=standard_text,
            ibron_cd=standard_value,
            notitie=standard_text,
            oe_best=standard_value,
            oe_bron=standard_value,
            omschrijving=standard_text,
        ),
        ibron=schemas.ibron.IbronIn(
            omschrijving=standard_text,
            oe_cd=standard_value,
            notitie=standard_text,
        ),
        oe_com_type=schemas.oe_com_type.OeComTypeIn(
            omschrijving=standard_text,
            notitie=standard_text,
        ),
        oe_koepel_oe=schemas.oe_koepel_oe.OeKoepelOeIn(
            notitie=standard_text,
            oe_cd=standard_value,
            oe_koepel_cd=standard_value,
        ),
        oe_koepel=schemas.oe_koepel.OeKoepelIn(titel=standard_text, omschrijving=standard_text),
        oe=schemas.oe.OeIn(
            afko=standard_text,
            e_contact=standard_text,
            huisnummer=standard_text,
            huisnummer_toev=standard_text,
            ibron_cd=standard_value,
            internet_domein=standard_text,
            lidw_sgebr=standard_text,
            naam_officieel=standard_text,
            naam_spraakgbr=standard_text,
            notitie=standard_text,
            plaats=standard_text,
            postcode=standard_text,
            provincie=standard_text,
            straat=standard_text,
            telefoon=standard_text,
        ),
        rge=schemas.rge.RgeIn(
            notitie=standard_text,
            re_link=standard_text,
            tekst=standard_text,
            titel=standard_text,
        ),
        ond=schemas.ond.OndIn(
            notitie=standard_text,
            sort_key=standard_value,
            omschrijving=standard_text,
            titel=standard_text,
        ),
        gg_evtp_sort=schemas.gg_evtp_sort.GgEvtpSortIn(
            gg_cd=standard_value,
            evtp_cd=standard_value,
            sort_key=standard_value,
        ),
        evtp_ond=schemas.evtp_ond.EvtpOndIn(
            evtp_cd=standard_value,
            versie_nr=standard_value,
            ond_cd=standard_value,
        ),
    )
    populated_payloads = populate_payloads(resource_pks, payloads)
    return populated_payloads


class TestAPI:
    def setup_method(self) -> None:
        self.headers: dict = {
            "accept": "application/json",
            "Authorization": "Bearer mock_token",
        }

    @pytest.mark.parametrize(
        "path, expected_content",
        [
            (f"/api/{TableResource.evtp_version.value}/", schemas.evtp_version.EvtpVersionWithRelations),
            (f"/api/{TableResource.evtp_gst.value}/", schemas.evtp_gst.EvtpGstWithRelations),
            # (f"/api/{TableResource.evtp_acc.value}/", schemas.evtp_acc.EvtpAccWithRelations),
            # (f"/api/{TableResource.evtp_oe_com_type.value}/", schemas.evtp_oe_com_type.EvtpOeComTypeWithRelations),
            (f"/api/{TableResource.oe.value}/", schemas.oe.OeWithRelations),
            # (f"/api/{TableResource.oe_com_type.value}/", schemas.oe_com_type.OeComType),
            # (f"/api/{TableResource.gg_koepel.value}/", schemas.gg.GgWithRelations),
            # (f"/api/{TableResource.gg.value}/", schemas.gg.GgWithRelations),
            (f"/api/{TableResource.gg_struct.value}/", schemas.gg_struct.GgStructWithRelations),
            # (f"/api/{TableResource.gg_evtp_sort.value}/", schemas.gg_evtp_sort.GgEvtpSortWithRelations),
            # (f"/api/{TableResource.gst.value}/", schemas.gst.GstWithRelations),
            (f"/api/{TableResource.rge.value}/", schemas.rge.Rge),
            # (f"/api/{TableResource.oe_struct.value}/", schemas.oe_struct.OeStructWithRelations),
            # (f"/api/{TableResource.ibron.value}/", schemas.ibron.IbronWithRelations),
            # (f"/api/{TableResource.gst_gg.value}/", schemas.gst_gg.GstGgWithRelations),
            (f"/api/{TableResource.gst_type.value}/", schemas.gst_type.GstType),
            # (f"/api/{TableResource.gst_gstt.value}/", schemas.gst_gstt.GstGsttWithRelations),
            (f"/api/{TableResource.ond.value}/", schemas.ond.Ond),
            # (f"/api/{TableResource.evtp_ond.value}/", schemas.evtp_ond.EvtpOndWithRelations),
        ],
    )
    def test_get_requests(self, client, path, expected_content, monkeypatch):
        # Send a GET request without authorization
        response = client.get(path, headers=self.headers)
        assert response.status_code == 200, "Get request has failed"

        response_json = response.json()

        # Assert that the response content is not empty
        assert response_json, "Response content is empty"

        if isinstance(response_json, list):
            # Deserialize the response content to a list
            response_content = [expected_content.model_validate(item) for item in response_json]
            assert response_content, "Deserialized response content is empty"
        else:
            # Deserialize the response content to a single object
            response_content = expected_content.model_validate(response_json)

        assert isinstance(response_content, list), "Response content does not match expected type list"

    @pytest.mark.parametrize(
        "path, expected_content",
        [
            (f"/api/{TableResource.evtp_version.value}/", schemas.evtp_version.EvtpVersion),
            (f"/api/{TableResource.evtp_gst.value}/", schemas.evtp_gst.EvtpGst),
            # (f"/api/{TableResource.evtp_acc.value}/", schemas.evtp_acc.EvtpAcc),
            # (f"/api/{TableResource.evtp_oe_com_type.value}/", schemas.evtp_oe_com_type.EvtpOeComType),
            (f"/api/{TableResource.oe.value}/", schemas.oe.Oe),
            # (f"/api/{TableResource.oe_com_type.value}/", schemas.oe_com_type.OeComType),
            # (f"/api/{TableResource.gg.value}/", schemas.gg.Gg),
            # (f"/api/{TableResource.gg_struct.value}/", schemas.gg_struct.GgStruct),
            # (f"/api/{TableResource.gg_evtp_sort.value}/", schemas.gg_evtp_sort.GgEvtpSort),
            # (f"/api/{TableResource.gst.value}/", schemas.gst.Gst),
            # (f"/api/{TableResource.rge.value}/", schemas.rge.Rge),
            # (f"/api/{TableResource.oe_struct.value}/", schemas.oe_struct.OeStruct),
            # (f"/api/{TableResource.ibron.value}/", schemas.ibron.Ibron),
            # (f"/api/{TableResource.gst_gg.value}/", schemas.gst_gg.GstGg),
            # (f"/api/{TableResource.gst_type.value}/", schemas.gst_type.GstType),
            # (f"/api/{TableResource.gst_gstt.value}/", schemas.gst_gstt.GstGstt),
            # (f"/api/{TableResource.ond.value}/", schemas.ond.Ond),
            # (f"/api/{TableResource.evtp_ond.value}/", schemas.evtp_ond.EvtpOnd),
        ],
    )
    def test_post_requests(self, client, path, expected_content, resource_payloads, monkeypatch):
        # Send a POST request
        payload_key = path.split("/")[-2].replace("-", "_")
        payload = resource_payloads.__dict__.get(payload_key, {})
        payload_json = payload.model_dump()
        response = client.post(path, json=payload_json, headers=self.headers)
        assert response.status_code == 200, "Post request has failed"

        # Assert that the response content is not empty
        response_json = response.json()
        assert response_json, "Response content is empty"

        # Deserialize the response content to a single object
        response_content = expected_content.model_validate(response_json)
        assert isinstance(response_content, expected_content), "Response content does not match the expected content"

        # Update the post_pk value in the ResourcePks instance
        # TODO

    @pytest.mark.parametrize(
        "path, pk",
        [
            (f"/api/{TableResource.evtp_gst.value}/", 1),
            # (f"/api/{TableResource.evtp_acc.value}/", schemas.evtp_acc.EvtpAcc),
            # (f"/api/{TableResource.evtp_oe_com_type.value}/", schemas.evtp_oe_com_type.EvtpOeComType),
            # (f"/api/{TableResource.oe.value}/", schemas.oe.Oe),
            # (f"/api/{TableResource.oe_com_type.value}/", schemas.oe_com_type.OeComType),
            # (f"/api/{TableResource.gg.value}/", 2),
            # (f"/api/{TableResource.gg_struct.value}/", schemas.gg_struct.GgStruct),
            # (f"/api/{TableResource.gg_evtp_sort.value}/", schemas.gg_evtp_sort.GgEvtpSort),
            # (f"/api/{TableResource.gst.value}/", 3),
            # (f"/api/{TableResource.rge.value}/", schemas.rge.Rge),
            # (f"/api/{TableResource.oe_struct.value}/", schemas.oe_struct.OeStruct),
            # (f"/api/{TableResource.ibron.value}/", schemas.ibron.Ibron),
            (f"/api/{TableResource.gst_gg.value}/", 2),
            # (f"/api/{TableResource.gst_type.value}/", schemas.gst_type.GstType),
            # (f"/api/{TableResource.gst_gstt.value}/", 3),
            # (f"/api/{TableResource.ond.value}/", schemas.ond.Ond),
            # (f"/api/{TableResource.evtp_ond.value}/", schemas.evtp_ond.EvtpOnd),
        ],
    )
    def test_delete_requests(self, client, path, pk, resource_pks, monkeypatch):
        # Send a DELETE request
        # TODO
        response = client.delete(f"{path}{pk}", headers=self.headers)
        assert response.status_code == 200, "Delete request has failed"


if __name__ == "__main__":
    pytest.main()
