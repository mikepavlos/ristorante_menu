from uuid import UUID

from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    description: str


class MenuRead(MenuBase):
    id: UUID
    submenus_count: int = 0
    dishes_count: int = 0

    class Config:
        orm_mode = True


class SubmenuBase(BaseModel):
    title: str
    description: str


class SubmenuRead(SubmenuBase):
    id: UUID
    dishes_count: int = 0

    class Config:
        orm_mode = True


class DishBase(BaseModel):
    title: str
    description: str
    price: str


class DishRead(DishBase):
    id: UUID

    class Config:
        orm_mode = True
