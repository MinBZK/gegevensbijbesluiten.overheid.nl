import pytest
from app.util.misc import create_upc, get_lower_hash, validate_url
from pydantic_core import PydanticCustomError


def test_get_lower_hash():
    hash_length = 10
    result = get_lower_hash(hash_length)
    assert len(result) == hash_length
    assert result.islower()
    assert result.isalpha()


def test_create_upc():
    result = create_upc()
    assert isinstance(result, int)
    assert len(str(result)) == 8


def test_validate_url_valid():
    valid_url = "https://www.example.com"
    result = validate_url(valid_url)
    assert result == valid_url


def test_validate_url_invalid():
    invalid_url = "invalid_url"
    with pytest.raises(PydanticCustomError):
        validate_url(invalid_url)


def test_validate_url_none():
    result = validate_url(None)
    assert result is None


def test_validate_url_empty():
    result = validate_url("")
    assert result is None
