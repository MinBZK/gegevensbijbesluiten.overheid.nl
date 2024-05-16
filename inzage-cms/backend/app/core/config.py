from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


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
