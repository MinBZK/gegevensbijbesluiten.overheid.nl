import app.models as models
import app.schemas as schemas
import pytest
from sqlalchemy import select


class TestEvtpVersionEndpoints:
    @pytest.fixture(autouse=True)
    def setup(self, db_sync):
        self.evtp_cd = db_sync.scalars(select(models.evtp.Evtp.evtp_cd)).first()
        self.oe_best = db_sync.scalars(select(models.oe.Oe.oe_cd)).first()
        self.versie_nr = 1

    def test_get_all(self, client):
        response = client.get("/api/evtp-version/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_list(self, client):
        response = client.get("/api/evtp-version-list/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_one(self, client):
        response = client.get(f"/api/evtp-version/{self.evtp_cd}")
        assert response.status_code == 200
        assert response.json() is not None

    # def test_update_one(self, client):
    #     body = schemas.evtp_version.EvtpVersionIn(
    #         self.versie_nr=1,
    #         evtp_nm="example_name",
    #         omschrijving="example_description",
    #         aanleiding="example_reason",
    #         gebr_dl="example_usage",
    #         oe_best= self.oe_best
    #     )
    #     response =  client.put(f"/api/evtp-version/{self.evtp_cd}", json=body.model_dump())
    #     print(response.json())
    #     assert response.status_code == 200
    #     assert response.json() is not None

    def test_one_partial(self, client):
        versie_nr = 1
        response = client.get(f"/api/evtp-version/partial/{self.evtp_cd}/{versie_nr}")
        assert response.status_code == 200
        assert response.json() is not None

    def test_get_filtered(self, client):
        search_query = "afval"
        response = client.get(f"/api/evtp-version/filter/{search_query}")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    # def test_create_one(self, client):
    #     body = schemas.evtp_version.EvtpVersionIn(
    #         self.versie_nr=1,
    #         evtp_nm="example_name",
    #         omschrijving="example_description",
    #         aanleiding="example_reason",
    #         gebr_dl="example_usage",
    #         oe_best= self.oe_best
    #     )
    #     response =  client.post("/api/evtp-version/", json=body.model_dump())
    #     assert response.status_code == 200
    #     assert response.json() is not None

    def test_duplicate(self, client):
        body = schemas.evtp_version.EvtpNewVersionIn(
            versie_nr=self.versie_nr,
            evtp_nm="example_name",
            omschrijving="example_description",
            aanleiding="example_reason",
            gebr_dl="example_usage",
            oe_best=self.oe_best,
        )
        response = client.post(f"/api/evtp-version-duplicate/{self.evtp_cd}", json=body.model_dump())
        assert response.status_code == 200
        assert response.json() is not None

    def test_get_all_including_all_versions(self, client):
        response = client.get("/api/evtp-version-list-versions/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_all_versions(self, client):
        response = client.get(f"/api/evtp-version-versions/{self.evtp_cd}")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_one_version(self, client):
        versie_nr = 1
        response = client.get(f"/api/evtp-version/{self.evtp_cd}/{versie_nr}")
        assert response.status_code == 200
        assert response.json() is not None

    # def test_create_new_version(self, client):
    #     body = schemas.evtp_version.EvtpNewVersionIn(
    #         versie_nr=self.versie_nr,
    #         evtp_nm="example_name",
    #         omschrijving="example_description",
    #         aanleiding="example_reason",
    #         gebr_dl="example_usage",
    #         oe_best= self.oe_best
    #     )
    #     response =  client.post(f"/api/evtp-version-version/{self.evtp_cd}", json=body.model_dump())
    #     assert response.status_code == 200
    #     assert response.json() is not None

    def test_get_tree_structure_one(self, client):
        response = client.get(f"/api/evtp-version/relations/{self.evtp_cd}/{self.versie_nr}")
        assert response.status_code == 200
        assert response.json() is not None

    def test_validate_tree_structure_one(self, client):
        response = client.get(f"/api/evtp-version/relations-validate/{self.evtp_cd}/{self.versie_nr}")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_change_id_pub(self, client):
        body = schemas.evtp_version.EvtpVersionStatus(
            evtp_cd=self.evtp_cd, versie_nr=self.versie_nr, evtp_nm="pytest", huidige_versie=True, id_publicatiestatus=1
        )  # Replace with valid data
        response = client.put(
            f"/api/evtp-version/change_id_pub/{self.evtp_cd}/{self.versie_nr}", json=body.model_dump()
        )
        assert response.status_code == 200
        assert response.json() == "OK"

    def test_get_evtp_by_publicatiestatus(self, client):
        response = client.get("/api/evtp-version/publicatiestatus/evtp/")
        assert response.status_code == 200
        assert response.json() is not None

    def test_get_evtp_by_publicatiestatus_organisation(self, client):
        response = client.get("/api/evtp-version/publicatiestatus/oe/")
        assert response.status_code == 200
        assert response.json() is not None
