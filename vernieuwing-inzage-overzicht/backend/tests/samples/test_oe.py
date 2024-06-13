import logging
from random import randint

import pytest
from app.crud.oe import get_all

logging = logging.getLogger(__name__)

RESOURCE_PAYLOADS = {
    "no_filter": {
        "limit": 20,
        "page": "1",
        "searchtext": "",
    },
    "search": {
        "limit": 20,
        "page": "1",
        "searchtext": "Belasting",
    },
}


@pytest.fixture()
def randomised_urls(db) -> list[str]:
    oe_list = get_all(db)
    urls = []
    for _ in range(10):
        oes_ind = randint(0, len(oe_list) - 1)
        oe_upc = oe_list[oes_ind].oe_upc
        urls.append(f"/api/oe/{oe_upc}/")
    return urls


@pytest.fixture()
def filters():
    return [
        ("/api/oe/filter", RESOURCE_PAYLOADS.get("no_filter")),
        ("/api/oe/filter", RESOURCE_PAYLOADS.get("search")),
    ]


class TestAPI:
    def test_detail_page(self, client, randomised_urls):
        """Test a random set of oe endpoints"""
        for url in randomised_urls:
            response = client.get(url)
            assert response.status_code == 200, "Get request has failed"
            response_json = response.json()
            assert response_json, "Response content is empty"
            assert isinstance(response_json, dict), "Response content does not match expected type list"

    # def test_searchbar(self, client, filters):
    #     """
    #     Test the filtering endpoint.
    #     posts multiple filters and compares to ensure that different filters return different results
    #     """
    #     results = []
    #     for path, filter_option in filters:
    #         response = client.post(path, json=filter_option)
    #         assert response.status_code == 200, "Get request has failed"
    #         response_object = json.loads(response.content)
    #         # Assert that the response content is not empty
    #         assert len(response_object["results"]) > 0, "Response content is empty"
    #         results.append(len(response_object["results"]))
    #     assert results[0] > results[1]


if __name__ == "__main__":
    pytest.main()
