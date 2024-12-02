import logging

logging = logging.getLogger(__name__)


class TestOe:
    def test_get_requests(self, client):
        """Test a random set of ond endpoints"""
        response = client.get("api/ond/populated")
        assert response.status_code == 200, "Get request has failed"
        response_json = response.json()
        assert response_json, "Response content is empty"

        response = client.get("api/ond/2")
        assert response.status_code == 200, "Get request has failed"
        response_json = response.json()
        assert response_json, "Response content is empty"
