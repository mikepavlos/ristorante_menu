from fastapi import Depends, HTTPException
from starlette import status

from menu_app.menu.cache_repository import clear_cache, get_cache, set_cache
from menu_app.menu.repository import DishCrud, MenuCrud, SubmenuCrud
from menu_app.menu.schemas import SubmenuWrite


class MenuService:
    def __init__(self, crud: MenuCrud = Depends()):
        self.crud = crud

    def list(self):
        if menu_cache := get_cache('menu:list'):
            return menu_cache

        menus = self.crud.all()
        set_cache('menu:list', [menu._asdict() for menu in menus])
        return menus

    def retrieve(self, menu_id):
        if menu_cache := get_cache(f'menu:{menu_id}'):
            return menu_cache

        menu = self.crud.get(menu_id)

        if menu is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='menu not found'
            )

        set_cache(f'menu:{menu_id}', menu._asdict())
        return menu

    def create(self, data):
        menu = self.crud.create(data)
        clear_cache('menu:list')
        return menu

    def update(self, menu_id, data):
        menu = self.crud.update(menu_id, data)
        if menu is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='menu not found'
            )

        clear_cache('menu:list')
        set_cache(f'menu:{menu.id}', menu)
        return menu

    def delete(self, menu_id):
        menu = self.crud.delete(menu_id)
        if menu is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='menu not found'
            )

        clear_cache(f'menu:{menu_id}')
        clear_cache('menu:list')
        return {
            'status': 'true',
            'message': 'The menu has been deleted'
        }


class SubmenuService:
    def __init__(self, crud: SubmenuCrud = Depends()):
        self.crud = crud

    def list(self):
        if submenu_cache := get_cache('submenu:list'):
            return submenu_cache

        submenus = self.crud.all()
        set_cache(
            'submenu:list',
            [submenu._asdict() for submenu in submenus]
        )
        return submenus

    def retrieve(self, submenu_id):
        if submenu_cache := get_cache(f'submenu:{submenu_id}'):
            return submenu_cache
        submenu = self.crud.get(submenu_id)
        if submenu is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='submenu not found'
            )
        set_cache(f'submenu:{submenu_id}', submenu._asdict())
        return submenu

    def create(self, menu_id, data):
        submenu = self.crud.create(menu_id, data)
        if submenu is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='menu not found'
            )
        clear_cache('submenu:list')
        clear_cache(f'menu:{menu_id}')
        clear_cache('menu:list')
        set_cache(f'submenu:{submenu.id}', submenu)
        return submenu

    def update(self, submenu_id, data: SubmenuWrite):
        submenu = self.crud.update(submenu_id, data)
        if submenu is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='submenu not found'
            )
        clear_cache('submenu:list')
        set_cache(f'submenu:{submenu_id}', submenu)
        return submenu

    def delete(self, submenu_id):
        submenu = self.crud.delete(submenu_id)
        if submenu is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='submenu not found'
            )
        clear_cache(f'submenu:{submenu_id}')
        clear_cache('submenu:list')
        clear_cache(f'menu:{submenu.menu_id}')
        clear_cache('menu:list')
        return {
            'status': 'true',
            'message': 'The submenu has been deleted'
        }


class DishService:
    def __init__(self, crud: DishCrud = Depends()):
        self.crud = crud

    def list(self):
        dishes = self.crud.all()
        return dishes

    def retrieve(self, dish_id):
        dish = self.crud.get(dish_id)
        if dish is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='dish not found'
            )
        return dish

    def create(self, submenu_id, data):
        dish = self.crud.create(submenu_id, data)
        if dish is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='submenu not found'
            )
        return dish

    def update(self, dish_id, data):
        dish = self.crud.update(dish_id, data)
        if dish is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='dish not found'
            )
        return dish

    def delete(self, dish_id):
        if not self.crud.delete(dish_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='dish not found'
            )
        return {
            'status': 'true',
            'message': 'The dish has been deleted'
        }
