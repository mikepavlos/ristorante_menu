from uuid import uuid4

from menu_app.menu import crud
from menu_app.menu.models import Menu
from menu_app.menu.services.base import submenus_count, dishes_count


def menu_list():
    menus = crud.db_all(Menu)

    for menu in menus:
        menu.submenus_count = submenus_count()
        menu.dishes_count = dishes_count()

    return menus


def menu_create(data):
    menu = Menu(
        id=uuid4(),
        title=data.title,
        description=data.description,
    )

    crud.db_create(menu)

    return menu


def menu_obj(menu_id):
    menu = crud.db_get_or_404(Menu, menu_id, 'menu')
    menu.submenus_count = submenus_count()
    menu.dishes_count = dishes_count()

    return menu


def menu_update(menu_id, data):
    menu = crud.db_get_or_404(Menu, menu_id, 'menu')

    menu.title = data.title
    menu.description = data.description
    menu.submenus_count = submenus_count()
    menu.dishes_count = dishes_count()

    crud.db_update(menu)

    return menu


def menu_delete(menu_id):
    menu = crud.db_get_or_404(Menu, menu_id, 'menu')

    crud.db_delete(menu)
