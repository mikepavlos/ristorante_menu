from uuid import uuid4

from menu_app.menu import crud
from menu_app.menu.models import Submenu, Dish


def dish_list():
    return crud.db_all(Dish)


def dish_create(submenu_id, data):
    crud.db_get_or_404(Submenu, submenu_id, 'submenu')

    dish = Dish(
        id=uuid4(),
        title=data.title,
        description=data.description,
        price=data.price,
        submenu_id=submenu_id
    )

    crud.db_create(dish)

    return dish


def dish_obj(dish_id):
    dish = crud.db_get_or_404(Dish, dish_id, 'dish')
    return dish


def dish_update(dish_id, data):
    dish = crud.db_get_or_404(Dish, dish_id, 'dish')
    dish.title = data.title
    dish.description = data.description
    dish.price = data.price

    crud.db_update(dish)

    return dish


def dish_delete(dish_id):
    dish = crud.db_get_or_404(Dish, dish_id, 'dish')

    crud.db_delete(dish)
