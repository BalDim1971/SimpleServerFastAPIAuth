import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

SQLALCHEMY_DATABASE_URL = (f"postgresql+psycopg2://"
                           f"{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Base = declarative_base()
#
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_db():
    # Создание БД при ее отсутствии.
    # Устанавливаем соединение с postgres
    conn = psycopg2.connect(user=DB_USER, password=DB_PASS)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    with conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM pg_catalog.pg_database "
                    f"WHERE datname = '{DB_NAME}'")
        result = cur.fetchone()
        if result[0] == 0:
            cur.execute(f"CREATE DATABASE {DB_NAME};")
            conn.commit()
        # else:
        #     print("БД с таким названием уже существует.")
    cur.close()
    conn.close()
