import logging

from app.schemas.common import SearchSuggestionsAllEntities
from tests.integration.config import ApiFilter

logging = logging.getLogger(__name__)


class TestCommon:
    def test_get_requests(self, client):
        """Test a random set of evtp and evtp_gst endpoints"""
        filter_option_1 = ApiFilter(endpoint="api/common/suggestion", params={"search_query": "afv"})
        response = client.get(filter_option_1.endpoint, params=filter_option_1.params)
        assert response.status_code == 200, "Get request has failed"
        result = SearchSuggestionsAllEntities.model_validate(response.json())
        assert result.evtp and len(result.evtp) > 0, "No evtp found"

        filter_option_2 = ApiFilter(endpoint="api/common/suggestion", params={"search_query": "gem"})
        response = client.get(filter_option_2.endpoint, params=filter_option_2.params)
        assert response.status_code == 200, "Get request has failed"
        result = SearchSuggestionsAllEntities.model_validate(response.json())
        assert result.oe and len(result.oe) > 0, "No oe found"
