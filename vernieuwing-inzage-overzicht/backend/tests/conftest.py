import logging
from typing import Any, Generator

import pytest
from app.app_factory import create_app
from app.database.database import get_sync_session
from fastapi.testclient import TestClient

logging = logging.getLogger(__name__)
app = create_app()


HEADERS = {
    "accept": "application/json",
    "Authorization": "Bearer mock_token",
}


@pytest.fixture
def db():
    return next(get_sync_session())


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, Any, None]:
    # Create a TestClient using the FastAPI app for testing
    with TestClient(app, headers=HEADERS) as test_client:
        yield test_client
