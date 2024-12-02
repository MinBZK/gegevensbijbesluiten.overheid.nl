import time
from unittest.mock import MagicMock, patch

import pytest
from app.api.exceptions import UserUnauthorizedException
from app.core.keycloak import _decode_token, _get_public_key, _update_public_key, cache, get_current_user
from jwt.exceptions import DecodeError, ExpiredSignatureError, ImmatureSignatureError


@pytest.fixture
def keycloak_openid_mock():
    return MagicMock()


@pytest.fixture
def token():
    return "test_token"


def test_update_public_key(keycloak_openid_mock):
    cache["keycloak_public_key_updated"] = time.time() - 31
    keycloak_openid_mock.public_key.return_value = "new_public_key"

    updated = _update_public_key(keycloak_openid_mock)

    assert updated is True
    assert cache["keycloak_public_key"] == "new_public_key"
    assert "keycloak_public_key_updated" in cache


def test_update_public_key_not_needed(keycloak_openid_mock):
    cache["keycloak_public_key_updated"] = time.time() - 10

    updated = _update_public_key(keycloak_openid_mock)

    assert updated is False


def test_get_public_key_cached(keycloak_openid_mock):
    cache["keycloak_public_key"] = "cached_public_key"
    cache["keycloak_public_key_updated"] = time.time()

    public_key = _get_public_key(keycloak_openid_mock)

    assert public_key == "cached_public_key"


@patch("app.core.keycloak._get_public_key")
@patch("app.core.keycloak.jwt.decode")
def test_decode_token_success(mock_jwt_decode, mock_get_public_key, token):
    mock_get_public_key.return_value = "public_key"
    mock_jwt_decode.return_value = {"user": "test_user"}

    decoded = _decode_token(token)

    assert decoded == {"user": "test_user"}


@patch("app.core.keycloak._get_public_key")
@patch("app.core.keycloak.jwt.decode")
def test_decode_token_expired(mock_jwt_decode, mock_get_public_key, token):
    mock_get_public_key.return_value = "public_key"
    mock_jwt_decode.side_effect = ExpiredSignatureError

    with pytest.raises(UserUnauthorizedException):
        _decode_token(token)


@patch("app.core.keycloak._get_public_key")
@patch("app.core.keycloak._update_public_key")
@patch("app.core.keycloak.jwt.decode")
def test_decode_token_decode_error(mock_jwt_decode, mock_update_public_key, mock_get_public_key, token):
    mock_get_public_key.return_value = "public_key"
    mock_jwt_decode.side_effect = DecodeError
    mock_update_public_key.return_value = True

    with patch("app.core.keycloak._decode_token", return_value={"user": "test_user"}):
        decoded = _decode_token(token)
        assert decoded == {"user": "test_user"}


@patch("app.core.keycloak._get_public_key")
@patch("app.core.keycloak.jwt.decode")
def test_decode_token_immature_signature(mock_jwt_decode, mock_get_public_key, token):
    mock_get_public_key.return_value = "public_key"
    mock_jwt_decode.side_effect = ImmatureSignatureError

    with patch("app.core.keycloak._decode_token", return_value={"user": "test_user"}):
        decoded = _decode_token(token)
        assert decoded == {"user": "test_user"}


@patch("app.core.keycloak._decode_token")
def test_get_current_user(mock_decode_token, token):
    mock_decode_token.return_value = {"prefered_username": "test_user"}

    user = get_current_user(token)

    assert user == {"prefered_username": "test_user"}
