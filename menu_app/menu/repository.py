from uuid import UUID

from fastapi import Depends
from sqlalchemy import delete, distinct, exc, func, insert, select, update
from sqlalchemy.orm import Session

from menu_app.database import get_session
from menu_app.menu.models import Dish, Menu, Submenu
from menu_app.menu.schemas import DishWrite, MenuWrite, SubmenuWrite


class MenuCrud:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self):
        query = (
            select(
                Menu.id,
                Menu.title,
                Menu.description,
                func.count(distinct(Submenu.id)).label('submenus_count'),
                func.count(distinct(Dish.id)).label('dishes_count'),
            )
            .outerjoin(Menu.submenus)
            .outerjoin(Submenu.dishes)
            .group_by(Menu.id)
        )
        return self.session.execute(query).all()

    def get(self, menu_id: str):
        query = (
            select(
                Menu.id,
                Menu.title,
                Menu.description,
                func.count(distinct(Submenu.id)).label('submenus_count'),
                func.count(distinct(Dish.id)).label('dishes_count'),
            )
            .where(Menu.id == menu_id)
            .outerjoin(Menu.submenus)
            .outerjoin(Submenu.dishes)
            .group_by(Menu.id)
        )
        return self.session.execute(query).first()

    def create(self, data: MenuWrite):
        stmt = (
            insert(Menu)
            .values(**data.model_dump())
            .returning(Menu)
        )
        menu = self.session.scalars(stmt)
        self.session.commit()
        return menu.first()

    def update(self, menu_id: str, data: MenuWrite):
        stmt = (
            update(Menu)
            .where(Menu.id == menu_id)
            .values(**data.model_dump())
            .returning(Menu)
        )
        menu = self.session.scalars(stmt)
        self.session.commit()
        return menu.first()

    def delete(self, menu_id: UUID):
        stmt = (
            delete(Menu)
            .where(Menu.id == menu_id)
            .returning(Menu)
        )
        menu = self.session.scalars(stmt)
        self.session.commit()
        return menu.first()


class SubmenuCrud:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self):
        query = (
            select(
                Submenu.id,
                Submenu.title,
                Submenu.description,
                func.count(distinct(Dish.id)).label('dishes_count'),
            )
            .outerjoin(Submenu.dishes)
            .group_by(Submenu.id)
        )
        return self.session.execute(query).all()

    def get(self, submenu_id: str):
        query = (
            select(
                Submenu.id,
                Submenu.title,
                Submenu.description,
                Submenu.menu_id,
                func.count(distinct(Dish.id)).label('dishes_count'),
            )
            .where(Submenu.id == submenu_id)
            .outerjoin(Submenu.dishes)
            .group_by(Submenu.id)
        )
        return self.session.execute(query).first()

    def create(self, menu_id: str, data: SubmenuWrite):
        stmt = (
            insert(Submenu)
            .values(
                **data.model_dump(),
                menu_id=menu_id,
            )
            .returning(Submenu)
        )

        try:
            submenu = self.session.scalars(stmt)
        except exc.IntegrityError:
            return

        self.session.commit()
        return submenu.first()

    def update(self, submenu_id: str, data: SubmenuWrite):
        stmt = (
            update(Submenu)
            .where(Submenu.id == submenu_id)
            .values(**data.model_dump())
            .returning(Submenu)
        )
        submenu = self.session.scalars(stmt)
        self.session.commit()
        return submenu.first()

    def delete(self, submenu_id: str):
        stmt = (
            delete(Submenu)
            .where(Submenu.id == submenu_id)
            .returning(Submenu)
        )
        submenu = self.session.scalars(stmt)
        self.session.commit()
        return submenu.first()


class DishCrud:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self):
        query = (
            select(
                Dish.id,
                Dish.title,
                Dish.description,
                Dish.price,
            )
        )
        return self.session.execute(query).all()

    def get(self, dish_id: str):
        return self.session.get(Dish, dish_id)

    def create(self, submenu_id: str, data: DishWrite):
        stmt = (
            insert(Dish)
            .values(
                **data.model_dump(),
                submenu_id=submenu_id,
            )
            .returning(Dish)
        )

        try:
            dish = self.session.scalars(stmt)
        except exc.IntegrityError:
            return

        self.session.commit()
        return dish.first()

    def update(self, dish_id: str, data: DishWrite):
        stmt = (
            update(Dish)
            .where(Dish.id == dish_id)
            .values(**data.model_dump())
            .returning(Dish)
        )
        dish = self.session.scalars(stmt)
        self.session.commit()
        return dish.first()

    def delete(self, dish_id: str):
        stmt = (
            delete(Dish)
            .where(Dish.id == dish_id)
            .returning(Dish)
        )
        dish = self.session.scalars(stmt)
        self.session.commit()
        return dish.first()
