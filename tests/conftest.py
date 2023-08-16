import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import Session, sessionmaker

from menu_app.database import Model, get_session
from menu_app.main import app
from menu_app.menu.models import Dish, Menu, Submenu
from menu_app.settings import settings

SQLALCHEMY_DATABASE_URL_TEST = (
    f'postgresql://'
    f'{settings.DB_USER_TEST}:{settings.DB_PASS_TEST}'
    f'@{settings.DB_HOST_TEST}:{settings.DB_PORT_TEST}'
    f'/{settings.DB_NAME_TEST}'
)
test_engine = create_engine(SQLALCHEMY_DATABASE_URL_TEST)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


def override_get_session():
    with TestingSessionLocal() as test_session:
        yield test_session


@pytest.fixture(autouse=True)
def setup_db():
    Model.metadata.drop_all(bind=test_engine)
    Model.metadata.create_all(bind=test_engine)
    yield
    session.close()
    Model.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    with TestClient(app) as client:
        app.dependency_overrides[get_session] = override_get_session
        yield client


session: Session = override_get_session().__next__()


@pytest.fixture
def menu():
    menu = session.scalars(
        insert(Menu)
        .values(
            title='test menu',
            description='test description'
        )
        .returning(Menu)
    )
    session.commit()
    return menu.first()


@pytest.fixture
def submenu(menu: Menu):
    submenu = session.scalars(
        insert(Submenu)
        .values(
            title='test submenu',
            description='test sub-description',
            menu_id=menu.id
        )
        .returning(Submenu)
    )
    session.commit()
    return submenu.first()


@pytest.fixture
def dish(submenu: Submenu):
    dish = session.scalars(
        insert(Dish)
        .values(
            title='test dish',
            description='test dish-description',
            price='10.99',
            submenu_id=submenu.id
        )
        .returning(Dish)
    )
    session.commit()
    return dish.first()


@pytest.fixture
def wrong_id():
    return '11111111-2222-3333-4444-555555555555'
