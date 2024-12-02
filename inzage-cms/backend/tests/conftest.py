import logging

import pytest
from app.app_factory import create_app
from app.database.database import get_async_session, get_sync_session
from fastapi.testclient import TestClient

logging = logging.getLogger(__name__)
app = create_app()


HEADERS = {
    "accept": "application/json",
    "Authorization": "Bearer mock_token",
}


@pytest.fixture
def db_sync():
    return next(get_sync_session())


@pytest.fixture(scope="session")
async def db_async():
    async for session in get_async_session():
        yield session


@pytest.fixture(scope="session")
def client():
    # Create a TestClient using the FastAPI app for testing
    with TestClient(app, headers=HEADERS) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def mock_keycloak_authorization(monkeypatch) -> None:
    def mock_decode_token(*args, **kwargs) -> dict[str, str]:
        return {
            "preferred_username": "pytest_user",
            "email": "pytest_user@ictu.nl",
        }

    monkeypatch.setattr("app.core.keycloak._decode_token", mock_decode_token)
