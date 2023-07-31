from menu_app.database import db
from menu_app.menu.models import Menu, Submenu, Dish


def submenus_count():
    return db.query(Menu.id == Submenu.menu_id).count()


def dishes_count():
    return (
        db.query(Dish.submenu_id == Submenu.id)
        .where(Menu.id == Submenu.menu_id)
        .count()
    )
