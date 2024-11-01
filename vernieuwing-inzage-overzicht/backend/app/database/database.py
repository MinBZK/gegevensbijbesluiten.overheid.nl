from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    sessionmaker,
)

from app.core.config import settings


def get_connection_string(
    use_async: bool = True,
) -> str:
    driver = "postgresql+asyncpg" if use_async else "postgresql"
    return f"{driver}://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"  # noqa


async_engine = create_async_engine(
    get_connection_string(),
    pool_size=10,  # Increase the pool size
    max_overflow=20,  # Increase the max overflow
    pool_timeout=30,  # Timeout for getting a connection from the pool
    pool_recycle=1800,  # Recycle connections after 30 minutes
    pool_pre_ping=True,
)
async_session = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    expire_on_commit=False,
)

synced_engine = create_engine(
    get_connection_string(use_async=False),
    pool_size=10,  # Increase the pool size
    max_overflow=20,  # Increase the max overflow
    pool_timeout=30,  # Timeout for getting a connection from the pool
    pool_recycle=1800,  # Recycle connections after 30 minutes
    pool_pre_ping=True,  # Enable connection health checks
)
synced_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=synced_engine,
)


class Base(DeclarativeBase):
    pass


async def get_async_session():
    async with async_session() as session:
        yield session


def get_sync_session() -> Generator:
    db = None
    try:
        db = synced_session()
        yield db
    finally:
        if db:
            db.close()
