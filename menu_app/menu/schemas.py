from uuid import UUID

from pydantic import BaseModel, ConfigDict


class MenuWrite(BaseModel):
    title: str
    description: str


class MenuReturn(MenuWrite):
    id: UUID


class MenuRead(MenuReturn):
    submenus_count: int = 0
    dishes_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class SubmenuWrite(BaseModel):
    title: str
    description: str


class SubmenuReturn(SubmenuWrite):
    id: UUID


class SubmenuRead(SubmenuReturn):
    dishes_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class DishWrite(BaseModel):
    title: str
    description: str
    price: str


class DishRead(DishWrite):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
