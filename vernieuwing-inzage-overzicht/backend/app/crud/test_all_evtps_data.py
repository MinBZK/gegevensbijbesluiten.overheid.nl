import logging

import requests

from app.schemas.evtp import EvtpQuery

logging = logging.getLogger(__name__)


class EndpointChecker:
    __slots__ = ["_url", "_payload"]

    def __init__(self, base_url: str):
        self._url = f"{base_url}api/evtp/filter"
        self._payload = EvtpQuery(limit=1000)

    def get_evtp_gst_upc(
        self,
    ) -> list[dict]:
        result = requests.post(
            self._url,
            json=self._payload.model_dump(),
        )
        return result.json().get("results")

    def check_endpoint(self, endpoint) -> None:
        response = requests.get(endpoint)

        if response.status_code == 200:
            data = response.json()
            if data:
                logging.info(f"Data is available for {endpoint}")
            else:
                assert False, f"No data available for {endpoint}"
        else:
            assert False, f"Failed to retrieve data from {endpoint}. Status code: {response.status_code}"
