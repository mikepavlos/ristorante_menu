from uuid import UUID

from fastapi import APIRouter, Depends, status

from menu_app.menu.menu_services import DishService
from menu_app.menu.schemas.schemas import DishIn, DishRead

router = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    tags=['dishes']
)


@router.get(
    '/',
    response_model=list[DishRead],
    status_code=status.HTTP_200_OK
)
def get_all_dishes(dish: DishService = Depends()):
    return dish.list()


@router.post(
    '/',
    response_model=DishRead,
    status_code=status.HTTP_201_CREATED
)
def create_dish(
        submenu_id: UUID,
        data: DishIn,
        dish: DishService = Depends()
):
    return dish.create(submenu_id, data)


@router.get(
    '/{dish_id}',
    response_model=DishRead,
    status_code=status.HTTP_200_OK
)
def get_dish(dish_id: UUID, dish: DishService = Depends()):
    return dish.retrieve(dish_id)


@router.patch(
    '/{dish_id}',
    response_model=DishRead,
    status_code=status.HTTP_200_OK
)
def update_dish(dish_id: UUID, data: DishIn, dish: DishService = Depends()):
    return dish.update(dish_id, data)


@router.delete('/{dish_id}', status_code=status.HTTP_200_OK)
def delete_dish(dish_id: UUID, dish: DishService = Depends()):
    return dish.delete(dish_id)
