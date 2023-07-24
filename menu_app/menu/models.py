from menu_app.database import Model
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Menu(Model):
    __tablename__ = 'menus'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4()
    )
    title = Column(String(50))
    description = Column(String(200))

    submenus = relationship(
        'Submenu',
        backref='menu',
        cascade='all, delete'
    )


class Submenu(Model):
    __tablename__ = 'submenus'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4()
    )
    title = Column(String(50))
    description = Column(String(200))
    menu_id = Column(UUID(as_uuid=True), ForeignKey('menus.id'))

    dishes = relationship(
        'Dish',
        backref='submenu',
        cascade='all, delete'
    )


class Dish(Model):
    __tablename__ = 'dishes'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4()
    )
    title = Column(String(50))
    description = Column(String(200))
    price = Column(Float(2))
    submenu_id = Column(UUID(as_uuid=True), ForeignKey('submenus.id'))
