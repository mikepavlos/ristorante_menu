import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from menu_app.database import Model


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
    menu_id = Column(
        UUID(as_uuid=True),
        ForeignKey('menus.id', ondelete='CASCADE')
    )

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
    price = Column(String(20))
    submenu_id = Column(
        UUID(as_uuid=True),
        ForeignKey('submenus.id', ondelete='CASCADE')
    )
