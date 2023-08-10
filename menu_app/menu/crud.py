from uuid import uuid4

from fastapi import Depends
from sqlalchemy import delete, distinct, exc, func, insert, select, update
from sqlalchemy.orm import Session

from menu_app.database import get_db
from menu_app.menu.models import Dish, Menu, Submenu
from menu_app.menu.schemas.schemas import DishIn, MenuIn, SubmenuIn


class MenuCrud:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def all(self):
        query = self.db.execute(
            select(
                Menu.id,
                Menu.title,
                Menu.description,
                func.count(distinct(Submenu.id)).label('submenus_count'),
                func.count(distinct(Dish.id)).label('dishes_count'),
            )
            .outerjoin(Submenu, Menu.id == Submenu.menu_id)
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .group_by(Menu.id)
        )
        return query.all()

    def get(self, menu_id):
        query = (
            select(
                Menu.id,
                Menu.title,
                Menu.description,
                func.count(distinct(Submenu.id)).label('submenus_count'),
                func.count(distinct(Dish.id)).label('dishes_count'),
            )
            .where(Menu.id == menu_id)
            .outerjoin(Submenu, Menu.id == Submenu.menu_id)
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .group_by(Menu.id)
        )

        try:
            obj = self.db.execute(query).first()
        except exc.InternalError:
            return

        return obj

    def create(self, data: MenuIn):
        stmt = (
            insert(Menu)
            .values(
                id=uuid4(),
                **data.dict()
            )
            .returning(Menu)
        )
        menu = self.db.execute(stmt).first()
        self.db.commit()
        return menu

    def update(self, menu_id: str, data: MenuIn):
        stmt = (
            update(Menu)
            .where(Menu.id == menu_id)
            .values(**data.dict())
            .returning(Menu)
        )

        try:
            menu = self.db.execute(stmt).one()
        except exc.NoResultFound:
            return

        self.db.commit()
        return menu

    def delete(self, menu_id: str):
        stmt = (
            delete(Menu)
            .where(Menu.id == menu_id)
            .returning(Menu)
        )

        try:
            self.db.execute(stmt).one()
        except exc.NoResultFound:
            return

        self.db.commit()
        return True


class SubmenuCrud:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def all(self):
        query = (
            select(
                Submenu.id,
                Submenu.title,
                Submenu.description,
                func.count(distinct(Dish.id)).label('dishes_count'),
            )
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .group_by(Submenu.id)
        )
        return self.db.execute(query).all()

    def get(self, submenu_id):
        query = (
            select(
                Submenu.id,
                Submenu.title,
                Submenu.description,
                func.count(distinct(Dish.id)).label('dishes_count'),
            )
            .where(Submenu.id == submenu_id)
            .outerjoin(Dish, Submenu.id == Dish.submenu_id)
            .group_by(Submenu.id)
        )
        return self.db.execute(query).first()

    def create(self, menu_id, data: SubmenuIn):
        menu = self.db.scalar((select(Menu.id)).where(Menu.id == menu_id))
        if not menu:
            return

        stmt = (
            insert(Submenu)
            .values(
                id=uuid4(),
                **data.dict(),
                menu_id=menu_id,
            )
            .returning(Submenu)
        )
        submenu = self.db.execute(stmt).first()
        self.db.commit()
        return submenu

    def update(self, submenu_id, data: SubmenuIn):
        stmt = (
            update(Submenu)
            .where(Submenu.id == submenu_id)
            .values(**data.dict())
            .returning(Submenu)
        )

        try:
            submenu = self.db.execute(stmt).one()
        except exc.NoResultFound:
            return

        self.db.commit()
        return submenu

    def delete(self, submenu_id):
        stmt = (
            delete(Submenu)
            .where(Submenu.id == submenu_id)
            .returning(Submenu)
        )

        try:
            self.db.execute(stmt).one()
        except (exc.NoResultFound, exc.DatabaseError):
            self.db.rollback()
            return

        self.db.commit()
        return True


class DishCrud:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def all(self):
        query = (
            select(
                Dish.id,
                Dish.title,
                Dish.description,
                Dish.price,
            )
        )
        return self.db.execute(query).all()

    def get(self, dish_id):
        query = (
            select(
                Dish.id,
                Dish.title,
                Dish.description,
                Dish.price,
            )
            .where(Dish.id == dish_id)
        )
        return self.db.execute(query).first()

    def create(self, submenu_id: str, data: DishIn):
        if not self.db.scalar(
            (select(Submenu.id))
            .where(Submenu.id == submenu_id)
        ):
            return

        stmt = (
            insert(Dish)
            .values(
                id=uuid4(),
                **data.dict(),
                submenu_id=submenu_id,
            )
            .returning(Dish)
        )
        dish = self.db.execute(stmt).first()
        self.db.commit()
        return dish

    def update(self, dish_id: str, data: DishIn):
        stmt = (
            update(Dish)
            .where(Dish.id == dish_id)
            .values(**data.dict())
            .returning(Dish)
        )

        try:
            dish = self.db.execute(stmt).one()
        except exc.NoResultFound:
            return

        self.db.commit()
        return dish

    def delete(self, dish_id: str):
        stmt = (
            delete(Dish)
            .where(Dish.id == dish_id)
            .returning(Dish)
        )

        try:
            self.db.execute(stmt).one()
        except exc.NoResultFound:
            return

        self.db.commit()
        return True
