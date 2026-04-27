import os
from concurrent.interpreters import create

from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from loguru import logger
from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession,async_sessionmaker
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

DB_HOST = os.getenv("POSTGRES_HOST")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORLD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_PORT = os.getenv("POSTGRES_PORT")

url = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORLD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_async_engine(
    url,
    echo=False,
    pool_size=10,
    max_overflow=5,
    pool_timeout=30
)

session_db = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

async def get_db():
    logger.debug("Открытие новой DB-сессии")
    async with session_db() as db:
        try:
            yield db
        finally:
            logger.debug("DB-сессия закрыта")