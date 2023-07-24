from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from menu_app.settings import settings

SQLALCHEMY_DATABASE_URL = (
    f'postgresql://'
    f'{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}'
    f'@{settings.POSTGRES_DB}:{settings.POSTGRES_PORT}'
    f'/{settings.POSTGRES_NAME}'
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()

Model = declarative_base()
