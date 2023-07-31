from uuid import UUID

from fastapi import APIRouter, status

from menu_app.menu.schemas import DishBase, DishRead
from menu_app.menu.services.dish import (
    dish_list,
    dish_create,
    dish_obj,
    dish_update,
    dish_delete
)

router = APIRouter()


@router.get(
    '/',
    response_model=list[DishRead],
    status_code=status.HTTP_200_OK
)
def get_all_dishes():
    return dish_list()


@router.post(
    '/',
    response_model=DishRead,
    status_code=status.HTTP_201_CREATED
)
def create_dish(submenu_id: UUID, dish: DishBase):
    return dish_create(submenu_id, dish)


@router.get(
    '/{dish_id}',
    response_model=DishRead,
    status_code=status.HTTP_200_OK
)
def get_dish(dish_id: UUID):
    return dish_obj(dish_id)


@router.patch(
    '/{dish_id}',
    response_model=DishRead,
    status_code=status.HTTP_200_OK
)
def update_dish(dish_id: UUID, dish: DishBase):
    return dish_update(dish_id, dish)


@router.delete('/{dish_id}', status_code=status.HTTP_200_OK)
def delete_dish(dish_id: UUID):
    dish_delete(dish_id)

    return {
        'status': 'true',
        'message': 'The dish has been deleted'
    }
