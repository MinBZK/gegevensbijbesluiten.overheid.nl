from random import choice, randint
from string import ascii_lowercase
from urllib.parse import urlparse

from pydantic_core import PydanticCustomError


def get_lower_hash(length: int) -> str:
    return "".join(choice(ascii_lowercase) for _ in range(length))


def create_upc() -> int:
    rl = []
    upc_id = ""
    for _ in range(0, 7):
        n = randint(0, 9)
        # Ensure the first digit is not 0
        if _ == 0 and n == 0:
            n = randint(1, 9)
        rl.append(str(n))
    e = int(rl[0]) + int(rl[2]) + int(rl[4]) + int(rl[6])
    o = int(rl[1]) + int(rl[3]) + int(rl[5])
    c = (e * 3 + o) % 10
    rl.append(str(c))
    return int(upc_id.join(rl))


def upc_check(upc_code: str) -> bool:
    r = []
    r[:] = upc_code
    e = int(r[0]) + int(r[2]) + int(r[4]) + int(r[6])
    o = int(r[1]) + int(r[3]) + int(r[5])
    c = (e * 3 + o) % 10
    return True if c == int(r[7]) else False


def validate_url(value: str | None):
    """
    Validates if the given value is a valid URL.
    Returns an empty string if the value is not a valid URL.
    """
    if value and urlparse(value).hostname:
        return value
    elif value is None or value == "":
        return None
    else:
        raise PydanticCustomError(
            "not_valid_link",
            "{field} is not a valid URL.",
            {"field": value},
        )
