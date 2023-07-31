from uuid import UUID

from fastapi import APIRouter, status

from menu_app.menu.schemas import MenuBase, MenuRead
from menu_app.menu.services.menu import (
    menu_list,
    menu_create,
    menu_obj,
    menu_update,
    menu_delete
)

router = APIRouter()


@router.get(
    '/',
    response_model=list[MenuRead],
    status_code=status.HTTP_200_OK
)
def get_all_menus():
    return menu_list()


@router.post(
    '/',
    response_model=MenuRead,
    status_code=status.HTTP_201_CREATED
)
def create_menu(menu: MenuBase):
    return menu_create(menu)


@router.get(
    '/{menu_id}',
    response_model=MenuRead,
    status_code=status.HTTP_200_OK
)
def get_menu(menu_id: UUID):
    return menu_obj(menu_id)


@router.patch(
    '/{menu_id}',
    response_model=MenuRead,
    status_code=status.HTTP_200_OK
)
def update_menu(menu_id: UUID, menu: MenuBase):
    return menu_update(menu_id, menu)


@router.delete('/{menu_id}', status_code=status.HTTP_200_OK)
def delete_menu(menu_id: UUID):
    menu_delete(menu_id)

    return {
        'status': 'true',
        'message': 'The menu has been deleted'
    }
