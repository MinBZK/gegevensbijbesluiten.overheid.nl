import json
import logging
from random import randint

import pytest
from app.crud.gg import get_all

logging = logging.getLogger(__name__)

RESOURCE_PAYLOADS = {
    "no_filter": {
        "limit": 20,
        "page": "1",
        "searchtext": "",
    },
    "search_afval": {
        "limit": 20,
        "page": "1",
        "searchtext": "afval",
    },
}


@pytest.fixture()
def randomised_urls(db) -> list[str]:
    gg_list = get_all(db)
    urls = []
    for _ in range(10):
        ggs_ind = randint(0, len(gg_list) - 1)
        gg_upc = gg_list[ggs_ind].gg_upc
        urls.append(f"/api/gg/{gg_upc}/")
    return urls


@pytest.fixture()
def filters():
    return [
        ("/api/gg/filter", RESOURCE_PAYLOADS.get("no_filter")),
        ("/api/gg/filter", RESOURCE_PAYLOADS.get("search_afval")),
    ]


class TestAPI:
    def test_get_requests(self, client, randomised_urls):
        """Test a random set of gg endpoints"""
        for url in randomised_urls:
            response = client.get(url)
            assert response.status_code == 200, "Get request has failed"
            response_json = response.json()
            assert response_json, "Response content is empty"
            assert isinstance(response_json, dict), "Response content does not match expected type list"

    def test_post_requests(self, client, filters):
        """
        Test the filtering endpoint.
        posts multiple filters and compares to ensure that different filters return different results
        """
        results = []
        for path, filter_option in filters:
            response = client.post(path, json=filter_option)
            assert response.status_code == 200, "Get request has failed"
            response_object = json.loads(response.content)
            # Assert that the response content is not empty
            assert len(response_object["result_gg"]) > 0, "Response content is empty"
            results.append(len(response_object["result_gg"]))
        assert results[0] > results[1]


if __name__ == "__main__":
    pytest.main()
