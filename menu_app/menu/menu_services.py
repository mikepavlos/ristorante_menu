from uuid import UUID

from fastapi import Depends, HTTPException
from starlette import status

from menu_app.menu.cache_repository import CacheResponse
from menu_app.menu.repository import DishCrud, MenuCrud, SubmenuCrud


class CheckExists:
    @staticmethod
    def is_exists(arg=None, obj_name: str = 'object'):
        if arg is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'{obj_name} not found'
            )


class MenuService:
    def __init__(
        self,
        cache: CacheResponse = Depends(),
        crud: MenuCrud = Depends(),
        check: CheckExists = Depends(),
    ):
        self.cache = cache
        self.crud = crud
        self.check = check

    def list(self):
        if menus_cache := self.cache.get('menu:list'):
            return menus_cache

        menus_db = self.crud.all()
        self.cache.set(
            key='menu:list',
            value=[menu._asdict() for menu in menus_db]
        )
        return menus_db

    def retrieve(self, menu_id):
        if menu_cache := self.cache.get(f'menu:{menu_id}'):
            return menu_cache

        menu_db = self.crud.get(menu_id)
        self.check.is_exists(menu_db, 'menu')
        self.cache.set(
            key=f'menu:{menu_id}',
            value=menu_db._asdict()
        )
        return menu_db

    def create(self, data):
        menu = self.crud.create(data)
        self.cache.clear('menu:list')
        return menu

    def update(self, menu_id, data):
        menu = self.crud.update(menu_id, data)
        self.check.is_exists(menu, 'menu')
        self.cache.clear(f'menu:{menu_id}')
        self.cache.clear('menu:list')
        return menu

    def delete(self, menu_id: UUID):
        menu = self.crud.delete(menu_id)
        self.check.is_exists(menu, 'menu')
        self.cache.clear(menu_id)
        self.cache.clear(':list')
        return {
            'status': 'true',
            'message': 'The menu has been deleted'
        }


class SubmenuService:
    def __init__(
        self,
        cache: CacheResponse = Depends(),
        crud: SubmenuCrud = Depends(),
        check: CheckExists = Depends(),
    ):
        self.crud = crud
        self.cache = cache
        self.check = check

    def list(self):
        if submenus_cache := self.cache.get('sub:list'):
            return submenus_cache

        submenus_db = self.crud.all()
        self.cache.set(
            key='sub:list',
            value=[submenu._asdict() for submenu in submenus_db]
        )
        return submenus_db

    def retrieve(self, submenu_id):
        if submenu_cache := self.cache.get(f'sub:{submenu_id}'):
            return submenu_cache

        submenu_db = self.crud.get(submenu_id)
        self.check.is_exists(submenu_db, 'submenu')
        self.cache.set(
            key=f'sub:{submenu_id}:{submenu_db.menu_id}',
            value=submenu_db._asdict()
        )
        return submenu_db

    def create(self, menu_id, data):
        submenu = self.crud.create(menu_id, data)
        self.check.is_exists(submenu, 'menu')
        self.cache.clear('sub:list')
        self.cache.clear('menu:list')
        self.cache.clear(f'menu:{menu_id}')
        return submenu

    def update(self, submenu_id, data):
        submenu = self.crud.update(submenu_id, data)
        self.check.is_exists(submenu, 'submenu')
        self.cache.clear(f'sub:{submenu_id}')
        self.cache.clear('sub:list')
        return submenu

    def delete(self, submenu_id):
        submenu = self.crud.delete(submenu_id)
        self.check.is_exists(submenu, 'submenu')
        self.cache.clear(submenu_id)
        self.cache.clear(f'menu:{submenu.menu_id}')
        self.cache.clear(':list')
        return {
            'status': 'true',
            'message': 'The submenu has been deleted'
        }


class DishService:
    def __init__(
        self,
        cache: CacheResponse = Depends(),
        crud: DishCrud = Depends(),
        check: CheckExists = Depends(),
    ):
        self.crud = crud
        self.cache = cache
        self.check = check

    def list(self):
        if dishes_cache := self.cache.get('dish:list'):
            return dishes_cache

        dishes_db = self.crud.all()
        self.cache.set(
            key='dish:list',
            value=[dish._asdict() for dish in dishes_db]
        )
        return dishes_db

    def retrieve(self, dish_id):
        if dish_cache := self.cache.get(f'dish:{dish_id}'):
            return dish_cache

        dish_db = self.crud.get(dish_id)
        self.check.is_exists(dish_db, 'dish')
        submenu = dish_db.submenu
        self.cache.set(
            key=f'dish:{dish_id}:{submenu.id}:{submenu.menu_id}',
            value=dish_db
        )
        return dish_db

    def create(self, submenu_id, data):
        dish = self.crud.create(submenu_id, data)
        self.check.is_exists(dish, 'submenu')
        self.cache.clear(f'sub:{submenu_id}')
        self.cache.clear(f'menu:{dish.submenu.menu_id}')
        self.cache.clear(':list')
        return dish

    def update(self, dish_id, data):
        dish = self.crud.update(dish_id, data)
        self.check.is_exists(dish, 'dish')
        self.cache.clear(f'dish:{dish_id}')
        self.cache.clear('dish:list')
        return dish

    def delete(self, dish_id):
        dish = self.crud.delete(dish_id)
        self.check.is_exists(dish, 'dish')
        self.cache.clear(dish_id)
        self.cache.clear(f'sub:{dish.submenu_id}')
        self.cache.clear(f'menu:{dish.submenu.menu_id}')
        self.cache.clear(':list')
        return {
            'status': 'true',
            'message': 'The dish has been deleted'
        }
