import logging

import pytest

from app import preditor

logging = logging.getLogger(__name__)


class TestAPI:
    def test_health_db(self, client):
        response = client.get("/api/health-db")
        assert response.status_code == 200, "Get request has failed"
        assert response.json() == "OK"

    # def test_health_evtp(self, client):
    #     response = client.get("/api/health-evtp")
    #     assert response.status_code == 200, "Get request has failed"
    #     assert response.json() == 'OK'

    def test_sitemap(self, client):
        response = client.get("/api/sitemap-urls")
        assert response.status_code == 200, "Get request has failed"
        assert len(response.json()) > 0

    def test_preditor(self, client):
        response = client.get(preditor.preditor_settings.get_url)
        assert response.status_code == 200, "Get request has failed"
        assert len(response.json()["nl"]) > 0


if __name__ == "__main__":
    pytest.main()