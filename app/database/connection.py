import os

from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


if not DB_NAME:
    raise ValueError("DB_NAME is missing from .env")

if not DB_USER:
    raise ValueError("DB_USER is missing from .env")

if not DB_PASSWORD:
    raise ValueError("DB_PASSWORD is missing from .env")


DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


def get_engine():
    return engine