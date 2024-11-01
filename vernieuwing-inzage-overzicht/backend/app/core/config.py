import os
from enum import Enum

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import (
    BaseSettings,
)

load_dotenv()
SIMILARITY_THRESHOLD: float = 0.30

if os.environ.get("CHANNEL") == "concept":
    PUBLICATION_RANGE = [2]
    CURRENT_VERSION = [True, False]
else:
    PUBLICATION_RANGE = [3]
    CURRENT_VERSION = [True]


class Pages(Enum):
    BESLUIT = "besluit"
    GEGEVENS = "gegevens"
    ORGANISATIES = "organisaties"


class Settings(BaseSettings):
    POSTGRES_SERVER: str = Field(alias="POSTGRES_SERVER")
    POSTGRES_DB: str = Field(alias="POSTGRES_DB")
    POSTGRES_PORT: int = Field(alias="POSTGRES_PORT")
    POSTGRES_USER: str = Field(alias="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(alias="POSTGRES_PASSWORD")

    class ConfigDict:  # type: ignore
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()  # type: ignore
