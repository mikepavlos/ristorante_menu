from uuid import UUID

from pydantic import BaseModel


class BaseData(BaseModel):
    title: str
    description: str


class BaseId(BaseModel):
    id: UUID


class BaseRead(BaseModel):
    class Config:
        orm_mode = True
