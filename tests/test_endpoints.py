from fastapi.testclient import TestClient

from menu_app.database import db, Model, engine
from menu_app.main import app
from menu_app.menu.models import Menu, Submenu, Dish

client = TestClient(app)

WRONG_ID = '11111111-2222-3333-4444-555555555555'

Model.metadata.drop_all(bind=engine)
Model.metadata.create_all(bind=engine)


def test_create_menu():
    data = {'title': 'test menu', 'description': 'test menu description'}
    response = client.post('/api/v1/menus/', json=data)
    assert response.status_code == 201

    menu = db.query(Menu).first()
    assert menu is not None

    data.update(
        id=str(menu.id),
        submenus_count=0,
        dishes_count=0
    )
    assert response.json() == data


def test_create_submenu():
    menu_id = db.query(Menu).first().id
    data = {'title': 'test submenu', 'description': 'test submenu description'}
    response = client.post(f'/api/v1/menus/{menu_id}/submenus/', json=data)
    assert response.status_code == 201

    submenu = db.query(Submenu).first()
    assert submenu is not None

    data.update(
        id=str(submenu.id),
        dishes_count=0
    )
    assert response.json() == data


def test_create_dish():
    submenu = db.query(Submenu).first()
    data = {
        'title': 'test dish',
        'description': 'test dish description',
        'price': 10.55
    }
    response = client.post(
        f'/api/v1/menus/{submenu.menu_id}/submenus/{submenu.id}/dishes/',
        json=data
    )
    assert response.status_code == 201

    dish = db.query(Dish).first()
    assert dish is not None

    data.update(
        id=str(dish.id),
        price=str(data['price'])
    )
    assert response.json() == data


def test_get_all_menus():
    response = client.get('/api/v1/menus/')
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


def test_get_all_submenus():
    menu_id = db.query(Menu).first().id
    response = client.get(f'/api/v1/menus/{menu_id}/submenus/')
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


def test_get_all_dishes():
    submenu = db.query(Submenu).first()
    response = client.get(
        f'/api/v1/menus/{submenu.menu_id}/submenus/{submenu.id}/dishes/'
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


def test_get_menu():
    menu_id = db.query(Menu).first().id
    response = client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200

    data = {
        'id': str(menu_id),
        'title': 'test menu',
        'description': 'test menu description',
        'submenus_count': 1,
        'dishes_count': 1
    }
    assert response.json() == data


def test_get_submenu():
    submenu = db.query(Submenu).first()
    response = client.get(
        f'/api/v1/menus/{submenu.menu_id}/submenus/{submenu.id}'
    )
    assert response.status_code == 200

    data = {
        'id': str(submenu.id),
        'title': 'test submenu',
        'description': 'test submenu description',
        'dishes_count': 1
    }
    assert response.json() == data


def test_get_dish():
    dish = db.query(Dish).first()
    submenu = dish.submenu
    response = client.get(
        f'/api/v1/'
        f'menus/{submenu.menu_id}/'
        f'submenus/{submenu.id}/'
        f'dishes/{dish.id}'
    )
    assert response.status_code == 200

    data = {
        'id': str(dish.id),
        'title': 'test dish',
        'description': 'test dish description',
        'price': str(dish.price)
    }
    assert response.json() == data


def test_get_menu_404():
    response = client.get(f'/api/v1/menus/{WRONG_ID}')
    assert response.status_code == 404
    assert response.json()['detail'] == 'menu not found'


def test_get_submenu_404():
    menu_id = db.query(Menu).first().id
    response = client.get(f'/api/v1/menus/{menu_id}/submenus/{WRONG_ID}')
    assert response.status_code == 404
    assert response.json()['detail'] == 'submenu not found'


def test_get_dish_404():
    submenu = db.query(Submenu).first()
    response = client.get(
        f'/api/v1/'
        f'menus/{submenu.menu_id}/'
        f'submenus/{submenu.id}/'
        f'dishes/{WRONG_ID}'
    )
    assert response.status_code == 404
    assert response.json()['detail'] == 'dish not found'


def test_update_menu():
    menu_id = db.query(Menu).first().id
    data = {
        'title': 'test update menu',
        'description': 'test update description',
    }
    response = client.patch(f'/api/v1/menus/{menu_id}', json=data)
    assert response.status_code == 200

    data.update(
        id=str(menu_id),
        submenus_count=1,
        dishes_count=1
    )
    assert response.json() == data


def test_update_submenu():
    submenu = db.query(Submenu).first()
    data = {
        'title': 'test update submenu',
        'description': 'test update submenu description',
    }
    response = client.patch(
        f'/api/v1/menus/{submenu.menu_id}/submenus/{submenu.id}',
        json=data
    )
    assert response.status_code == 200

    data.update(
        id=str(submenu.id),
        dishes_count=1
    )
    assert response.json() == data


def test_update_dish():
    dish = db.query(Dish).first()
    data = {
        'title': 'test update dish',
        'description': 'test update dish description',
        'price': 20.22
    }
    response = client.patch(
        f'/api/v1/'
        f'menus/{dish.submenu.menu_id}/'
        f'submenus/{dish.submenu_id}/'
        f'dishes/{dish.id}',
        json=data
    )
    assert response.status_code == 200

    data.update(
        id=str(dish.id),
        price=str(data['price'])
    )
    assert response.json() == data


def test_delete_dish():
    dish = db.query(Dish).first()
    response = client.delete(
        f'/api/v1/'
        f'menus/{dish.submenu.menu_id}/'
        f'submenus/{dish.submenu_id}/'
        f'dishes/{dish.id}'
    )
    assert response.status_code == 200
    assert response.json() == {
        'status': 'true',
        'message': 'The dish has been deleted'
    }


def test_submenu_deleted_dish_counts():
    submenu = db.query(Submenu).first()
    response = client.get(
        f'/api/v1/menus/{submenu.menu_id}/submenus/{submenu.id}'
    )
    assert response.json()['dishes_count'] == 0


def test_menu_deleted_dish_counts():
    menu_id = db.query(Menu).first().id
    response = client.get(f'/api/v1/menus/{menu_id}')
    assert response.json()['submenus_count'] == 1
    assert response.json()['dishes_count'] == 0


def test_delete_submenu():
    submenu = db.query(Submenu).first()
    response = client.delete(
        f'/api/v1/menus/{submenu.menu_id}/submenus/{submenu.id}'
    )
    assert response.status_code == 200
    assert response.json() == {
        'status': 'true',
        'message': 'The submenu has been deleted'
    }


def test_menu_deleted_submenu_counts():
    menu_id = db.query(Menu).first().id
    response = client.get(f'/api/v1/menus/{menu_id}')
    assert response.json()['submenus_count'] == 0
    assert response.json()['dishes_count'] == 0


def test_delete_menu():
    menu_id = db.query(Menu).first().id
    response = client.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    assert response.json() == {
        'status': 'true',
        'message': 'The menu has been deleted'
    }
