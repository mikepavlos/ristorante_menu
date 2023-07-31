from uuid import uuid4

from menu_app.menu import crud
from menu_app.menu.models import Menu, Submenu
from menu_app.menu.services.base import dishes_count


def submenu_list():
    submenus = crud.db_all(Submenu)

    for submenu in submenus:
        submenu.dishes_count = dishes_count()

    return submenus


def submenu_create(menu_id, data):
    crud.db_get_or_404(Menu, menu_id, 'menu')

    submenu = Submenu(
        id=uuid4(),
        title=data.title,
        description=data.description,
        menu_id=menu_id
    )

    crud.db_create(submenu)

    return submenu


def submenu_obj(submenu_id):
    submenu = crud.db_get_or_404(Submenu, submenu_id, 'submenu')
    submenu.dishes_count = dishes_count()

    return submenu


def submenu_update(submenu_id, data):
    submenu = crud.db_get_or_404(Submenu, submenu_id, 'submenu')
    submenu.title = data.title
    submenu.description = data.description
    submenu.dishes_count = dishes_count()

    crud.db_update(submenu)

    return submenu


def submenu_delete(submenu_id):
    submenu = crud.db_get_or_404(Submenu, submenu_id, 'submenu')

    crud.db_delete(submenu)
