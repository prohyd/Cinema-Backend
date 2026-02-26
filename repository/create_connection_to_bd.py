import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from loguru import logger
from pathlib import Path
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORLD = os.getenv("DB_PASSWORLD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

logger.info("Загрузка конфигурации базы данных из .env")

url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORLD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
logger.info("Создание SQLAlchemy engine")
engine = create_engine(
    url,
    echo=False,
    pool_size=10,
    max_overflow=5,
    pool_timeout=30
)
logger.success("Engine успешно создан")

session_db = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

logger.success("Sessionmaker успешно настроен")

def get_bd():
    logger.debug("Открытие новой DB-сессии")
    db = session_db()
    try:
        yield db
    finally:
        db.close()
        logger.debug("DB-сессия закрыта")