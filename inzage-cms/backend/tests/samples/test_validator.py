import logging
from random import randint

import pytest
from sqlalchemy import select

import app.models as models
from app.config.resource import TableResource

logging = logging.getLogger(__name__)


@pytest.fixture()
def randomised_urls(db) -> list[str]:
    evtp_list = db.scalars(select(models.evtp.Evtp.evtp_cd)).all()
    urls = []
    for _ in range(5):
        evtp_index = randint(0, len(evtp_list) - 1)
        evtp_cd = evtp_list[evtp_index]
        urls.append(f"/api/{TableResource.evtp_version.value}/relations-validate/{evtp_cd}/1")
    return urls


class TestAPI:
    def test_get_requests(self, client, randomised_urls):
        """Test a random set of evtp version endpoints"""
        urls = randomised_urls
        for url in urls:
            response = client.get(url)
            assert response.status_code == 200, "Get request has failed"


if __name__ == "__main__":
    pytest.main()
