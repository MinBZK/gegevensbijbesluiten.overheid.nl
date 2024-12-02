import logging
from random import randint

import app.models as models
import pytest
from app.config.resource import MappingPublicatiestatus, TableResource
from sqlalchemy import select

logging = logging.getLogger(__name__)


@pytest.fixture()
def randomised_urls(db_sync) -> list[str]:
    evtp_list = db_sync.scalars(
        select(models.evtp.EvtpVersion.evtp_cd).filter(
            models.evtp.EvtpVersion.id_publicatiestatus < MappingPublicatiestatus.ARCHIVED.code
        )
    ).all()
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
