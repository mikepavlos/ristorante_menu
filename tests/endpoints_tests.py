from sqlalchemy import select

from menu_app.menu.models import Dish, Menu, Submenu
from tests.conftest import session


class TestMenuEndpoints:

    def test_get_all_menus(self, client, menu):
        response = client.get('/api/v1/menus/')
        response_menus = response.json()
        assert response.status_code == 200
        assert isinstance(response_menus, list)
        assert len(response_menus) == 1
        assert response_menus[0]['id'] == str(menu.id)
        assert response_menus[0]['title'] == menu.title
        assert response_menus[0]['description'] == menu.description
        assert response_menus[0]['submenus_count'] == 0
        assert response_menus[0]['dishes_count'] == 0

    def test_create_menu(self, client):
        data = {
            'title': 'test create menu',
            'description': 'test create description'
        }
        response = client.post('/api/v1/menus/', json=data)
        response_menu = response.json()
        menu_id = session.scalar(select(Menu.id))
        assert response.status_code == 201
        assert response_menu['id'] == str(menu_id)
        assert response_menu['title'] == data['title']
        assert response_menu['description'] == data['description']

    def test_get_menu(self, client, menu):
        response = client.get(f'/api/v1/menus/{menu.id}')
        response_menu = response.json()
        assert response.status_code == 200
        assert response_menu['id'] == str(menu.id)
        assert response_menu['title'] == menu.title
        assert response_menu['description'] == menu.description
        assert response_menu['submenus_count'] == 0
        assert response_menu['dishes_count'] == 0

    def test_get_menu_not_found(self, client, wrong_id):
        response = client.get(f'/api/v1/menus/{wrong_id}')
        assert response.status_code == 404
        assert response.json()['detail'] == 'menu not found'

    def test_update_menu(self, client, menu):
        data = {
            'title': 'test update menu',
            'description': 'test update description',
        }
        response = client.patch(f'/api/v1/menus/{menu.id}', json=data)
        assert response.status_code == 200

        data.update(id=str(menu.id))
        assert response.json() == data

    def test_update_menu_not_found(self, client, wrong_id):
        data = {
            'title': 'test update menu',
            'description': 'test update description',
        }
        response = client.patch(f'/api/v1/menus/{wrong_id}', json=data)
        assert response.status_code == 404
        assert response.json()['detail'] == 'menu not found'

    def test_delete_menu(self, client, menu):
        response = client.delete(f'/api/v1/menus/{menu.id}')
        assert response.status_code == 200
        assert response.json() == {
            'status': 'true',
            'message': 'The menu has been deleted'
        }

    def test_delete_menu_not_found(self, client, wrong_id):
        response = client.delete(f'/api/v1/menus/{wrong_id}')
        assert response.status_code == 404
        assert response.json()['detail'] == 'menu not found'


class TestSubmenuEndpoints:

    def test_get_all_submenus(self, client, submenu: Submenu):
        response = client.get('/api/v1/menus/menu_id/submenus/')
        response_submenus = response.json()
        assert response.status_code == 200
        assert isinstance(response_submenus, list)
        assert len(response_submenus) == 1
        assert response_submenus[0]['id'] == str(submenu.id)
        assert response_submenus[0]['title'] == submenu.title
        assert response_submenus[0]['description'] == submenu.description
        assert response_submenus[0]['dishes_count'] == 0

    def test_create_submenu(self, client, menu: Menu):
        data = {
            'title': 'test create submenu',
            'description': 'test create submenu description'
        }
        response = client.post(
            f'/api/v1/menus/{menu.id}/submenus/',
            json=data
        )
        response_submenu = response.json()
        submenu_id = session.scalar(select(Submenu.id))
        assert response.status_code == 201
        assert response_submenu['id'] == str(submenu_id)
        assert response_submenu['title'] == data['title']
        assert response_submenu['description'] == data['description']

    def test_create_submenu_not_found(self, client, wrong_id):
        data = {
            'title': 'test create submenu',
            'description': 'test create submenu description'
        }
        response = client.post(
            f'/api/v1/menus/{wrong_id}/submenus/',
            json=data
        )
        assert response.status_code == 404
        assert response.json()['detail'] == 'menu not found'

    def test_get_submenu(
            self,
            client,
            submenu: Submenu
    ):
        response = client.get(
            f'/api/v1/menus/menu_id'
            f'/submenus/{submenu.id}'
        )
        response_submenu = response.json()
        assert response.status_code == 200
        assert response_submenu['id'] == str(submenu.id)
        assert response_submenu['title'] == submenu.title
        assert response_submenu['description'] == submenu.description
        assert response_submenu['dishes_count'] == 0

    def test_get_submenu_not_found(self, client, menu, wrong_id):
        response = client.get(
            f'/api/v1/menus/menu.id'
            f'/submenus/{wrong_id}'
        )
        assert response.status_code == 404
        assert response.json()['detail'] == 'submenu not found'

    def test_update_submenu(self, client, submenu):
        data = {
            'title': 'test update submenu',
            'description': 'test update submenu description',
        }
        response = client.patch(
            f'/api/v1/menus/menu_id'
            f'/submenus/{submenu.id}',
            json=data
        )
        data.update(id=str(submenu.id))
        assert response.status_code == 200
        assert response.json() == data

    def test_update_submenu_not_found(
            self,
            client,
            wrong_id
    ):
        data = {
            'title': 'test update submenu',
            'description': 'test update submenu description',
        }
        response = client.patch(
            f'/api/v1/menus/menu_id/submenus/{wrong_id}',
            json=data
        )
        assert response.status_code == 404
        assert response.json()['detail'] == 'submenu not found'

    def test_delete_submenu(self, client, submenu: Submenu):
        response = client.delete(
            f'/api/v1/'
            f'menus/menu_id'
            f'/submenus/{submenu.id}'
        )
        assert response.status_code == 200
        assert response.json() == {
            'status': 'true',
            'message': 'The submenu has been deleted'
        }

    def test_delete_submenu_not_found(self, client, wrong_id):
        response = client.delete(
            f'/api/v1/menus/menu.id/submenus/{wrong_id}',
        )
        assert response.status_code == 404
        assert response.json()['detail'] == 'submenu not found'


class TestDishEndpoints:

    def test_get_all_dishes(self, client, dish: Dish):
        response = client.get(
            '/api/v1/menus/menu_id/submenus/submenu_id/dishes/'
        )
        response_dishes = response.json()
        assert response.status_code == 200
        assert isinstance(response_dishes, list)
        assert len(response_dishes) == 1
        assert response_dishes[0]['id'] == str(dish.id)
        assert response_dishes[0]['title'] == dish.title
        assert response_dishes[0]['description'] == dish.description
        assert response_dishes[0]['price'] == dish.price

    def test_create_dish(self, client, submenu: Submenu):
        data = {
            'title': 'create dish',
            'description': 'dish description',
            'price': '20.99'
        }
        response = client.post(
            f'/api/v1'
            f'/menus/menu_id'
            f'/submenus/{submenu.id}'
            f'/dishes/',
            json=data
        )
        response_dishes = response.json()
        dish_id = session.scalar(select(Dish.id))
        assert response.status_code == 201
        assert response_dishes['id'] == str(dish_id)
        assert response_dishes['title'] == data['title']
        assert response_dishes['description'] == data['description']
        assert response_dishes['price'] == data['price']

    def test_create_dish_not_found(self, client, submenu, wrong_id):
        data = {
            'title': 'create dish',
            'description': 'dish description',
            'price': '20.99'
        }
        response = client.post(
            f'/api/v1'
            f'/menus/menu_id'
            f'/submenus/{wrong_id}'
            f'/dishes/',
            json=data
        )
        assert response.status_code == 404
        assert response.json()['detail'] == 'submenu not found'

    def test_get_dish(self, client, dish: Dish):
        response = client.get(
            f'/api/v1/'
            f'menus/menu_id/'
            f'submenus/submenu_id/'
            f'dishes/{dish.id}'
        )
        response_dish = response.json()
        assert response.status_code == 200
        assert response_dish['id'] == str(dish.id)
        assert response_dish['title'] == dish.title
        assert response_dish['description'] == dish.description
        assert response_dish['price'] == dish.price

    def test_get_dish_not_found(self, client, wrong_id):
        response = client.get(
            f'/api/v1/'
            f'menus/menu_id/'
            f'submenus/submenu_id/'
            f'dishes/{wrong_id}'
        )
        assert response.status_code == 404
        assert response.json()['detail'] == 'dish not found'

    def test_update_dish(self, client, dish):
        data = {
            'title': 'test update dish',
            'description': 'test update dish description',
            'price': '30.99'
        }
        response = client.patch(
            f'/api/v1/'
            f'menus/menu_id/'
            f'submenus/submenu_id/'
            f'dishes/{dish.id}',
            json=data
        )
        data.update(id=str(dish.id))
        assert response.status_code == 200
        assert response.json() == data

    def test_update_dish_not_found(self, client, wrong_id):
        data = {
            'title': 'test update dish',
            'description': 'test update dish description',
            'price': '30.99'
        }
        response = client.patch(
            f'/api/v1/'
            f'menus/menu_id/'
            f'submenus/submenu_id/'
            f'dishes/{wrong_id}',
            json=data
        )
        assert response.status_code == 404
        assert response.json()['detail'] == 'dish not found'

    def test_delete_dish(self, client, dish: Dish):
        response = client.delete(
            f'/api/v1/'
            f'menus/menu_id/'
            f'submenus/submenu_id/'
            f'dishes/{dish.id}'
        )
        assert response.status_code == 200
        assert response.json() == {
            'status': 'true',
            'message': 'The dish has been deleted'
        }

    def test_delete_dish_not_found(self, client, wrong_id):
        response = client.delete(
            f'/api/v1/'
            f'menus/menu_id/'
            f'submenus/submenu_id/'
            f'dishes/{wrong_id}'
        )
        assert response.status_code == 404
        assert response.json()['detail'] == 'dish not found'


class TestCounts:

    def test_menu_counts(self, client, dish: Dish):
        endpoint = f'/api/v1/menus/{dish.submenu.menu_id}/'

        response_menu = client.get(endpoint)
        assert response_menu.json()['submenus_count'] == 1
        assert response_menu.json()['dishes_count'] == 1

        client.delete(
            f'/api/v1/'
            f'menus/menu_id/'
            f'submenus/submenu_id/'
            f'dishes/{dish.id}'
        )
        response_deleted_dish = client.get(endpoint)
        assert response_deleted_dish.json()['submenus_count'] == 1
        assert response_deleted_dish.json()['dishes_count'] == 0

        client.delete(
            f'/api/v1/'
            f'menus/menu_id'
            f'/submenus/{dish.submenu.id}'
        )
        response_deleted_submenu = client.get(endpoint)
        assert response_deleted_submenu.json()['submenus_count'] == 0
        assert response_deleted_submenu.json()['dishes_count'] == 0
