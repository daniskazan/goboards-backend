from asyncio import current_task
from typing import Generator

from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
)
from sqlalchemy.ext.asyncio.engine import create_async_engine

from configs.server import ServerConfig

async_engine = create_async_engine(ServerConfig.DB_URL, echo=ServerConfig.DEBUG)
AsyncSessionFactory: async_sessionmaker = async_sessionmaker(bind=async_engine, expire_on_commit=False)
DatabaseConnection = async_scoped_session(session_factory=AsyncSessionFactory, scopefunc=current_task)


async def get_db() -> Generator:
    yield DatabaseConnection
    await DatabaseConnection.close()
