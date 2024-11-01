import io
import json
import logging
import random

import pandas as pd
import pytest
from app.crud.sitemap import get_evtps
from app.utils.decorators import timeit, timeit_once

logging = logging.getLogger(__name__)


RESOURCE_PAYLOADS = {
    "no_filter": {
        "organisation": "",
        "limit": 20,
        "page": "1",
        "searchtext": "",
    },
    "filter_burgerzaken": {
        "organisation": "Gemeente (burgerzaken)",
        "limit": 20,
        "page": "1",
        "searchtext": "",
    },
    "search_afval": {
        "organisation": "",
        "limit": 20,
        "page": "1",
        "searchtext": "afval",
    },
}


# '/api/evtp-tree/61846917/gst/4763'
@pytest.fixture()
def randomised_urls(db):
    evtps = get_evtps(db)
    urls = []
    for _ in range(15):
        evtps_ind = random.randint(0, len(evtps) - 1)
        gst_ind = random.randint(0, len(evtps[evtps_ind].entities_evtp_gst) - 1)

        evtp_upc = evtps[evtps_ind].evtp_upc
        gst_upc = evtps[evtps_ind].entities_evtp_gst[gst_ind].entity_gst.gst_upc
        version = evtps[evtps_ind].versie_nr
        urls.append(f"/api/evtp-tree/{evtp_upc}/gg/")
        urls.append(f"/api/evtp-tree/{evtp_upc}/{version}/gg/")
        urls.append(f"/api/evtp-tree/{evtp_upc}/gst/{gst_upc}")
        urls.append(f"/api/evtp-tree/{evtp_upc}/{version}/gst/{gst_upc}")

    yield urls


@pytest.fixture()
def filters():
    return [
        ("/api/evtp/filter", RESOURCE_PAYLOADS.get("no_filter")),
        ("/api/evtp/filter", RESOURCE_PAYLOADS.get("filter_burgerzaken")),
        ("/api/evtp/filter", RESOURCE_PAYLOADS.get("search_afval")),
    ]


class TestAPI:
    @timeit_once
    def test_get_requests(self, client, randomised_urls):
        """Test a random set of evtp and evtp_gst endpoints"""
        for url in randomised_urls:
            response = client.get(url)
            assert response.status_code == 200, "Get request has failed"
            response_json = response.json()
            assert response_json, "Response content is empty"
            assert isinstance(response_json, dict), "Response content does not match expected type list"

    @timeit
    def test_evtp_download(self, client):
        """Test download functionality"""
        response = client.get("/api/evtp/file")
        assert response.status_code == 200, "Get request has failed"
        df = pd.read_csv(io.StringIO(response.content.decode("utf-8-sig")))
        assert df.shape[0] > 1
        assert "unieke_code" in df.columns

    # TODO, testdata does not contain any onderdelen
    # def test_onderdelen(self, client):
    #     """Test fetch onderdelen"""
    #     response = client.get("/api/ond/populated")
    #     assert response.status_code == 200, "Get request has failed"
    #     for ond_cd in random.sample(response.content, 5):
    #         response = client.get(f"/api/ond/{ond_cd}")
    #         assert response.status_code == 200, "request has failed"

    def test_count(self, client):
        """fetch number of evtp"""
        response = client.get("/api/evtp/count")
        assert response.status_code == 200, "Get request has failed"
        assert response.json() > 0

    def test_statistics(self, client):
        """fetch evtp statistics"""
        response = client.get("/api/evtp/statistics-per-oe")
        assert response.status_code == 200, "Get request has failed"
        assert len(response.json()["oe_by_evtp_total"]) > 0
        # assert isinstance(response.json()['oe_by_evtp_total'][0], schemas.oe.OeByEvtpTotal), "Response content does not match expected type list"

    def test_post_requests(self, client, filters):
        """
        Test the filtering endpoint.
        posts multiple filters and compares to ensure that different filters return different results
        """
        results = []
        for path, filter_option in filters:
            logging.info(f"filter options: {filter_option}")
            response = client.post(path, json=filter_option)
            assert response.status_code == 200, "Get request has failed"
            response_object = json.loads(response.content)
            # Assert that the response content is not empty
            assert len(response_object["result_evtp"]) > 0, f"Response content for {filter_option} is empty"
            results.append(len(response_object["result_evtp"]))
        assert results[0] != results[1] != results[2]


if __name__ == "__main__":
    pytest.main()
