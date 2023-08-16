from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from menu_app.settings import settings

SQLALCHEMY_DATABASE_URL = (
    f'postgresql+psycopg2://'
    f'{settings.DB_USER}:{settings.DB_PASS}'
    f'@{settings.DB_HOST}:{settings.DB_PORT}'
    f'/{settings.DB_NAME}'
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    with SessionLocal() as session:
        yield session


class Model(DeclarativeBase):
    pass
