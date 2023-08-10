from menu_app.menu.schemas import base
from menu_app.menu.schemas.base import BaseData, BaseId, BaseRead


class MenuIn(BaseData):
    ...


class MenuOut(MenuIn, BaseId):
    ...


class MenuRead(MenuOut, BaseRead):
    submenus_count: int = 0
    dishes_count: int = 0


class SubmenuIn(base.BaseData):
    ...


class SubmenuOut(SubmenuIn, base.BaseId):
    ...


class SubmenuRead(SubmenuOut, BaseRead):
    dishes_count: int = 0


class DishIn(base.BaseData):
    price: str


class DishRead(DishIn, BaseId, BaseRead):
    ...
