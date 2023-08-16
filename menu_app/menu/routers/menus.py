from uuid import UUID

from fastapi import APIRouter, Depends, status

from menu_app.menu.menu_services import MenuService
from menu_app.menu.schemas import MenuRead, MenuReturn, MenuWrite

router = APIRouter(prefix='/api/v1/menus', tags=['menus'])


@router.get(
    '/',
    response_model=list[MenuRead],
    status_code=status.HTTP_200_OK
)
def get_all_menus(menu: MenuService = Depends()):
    return menu.list()


@router.post(
    '/',
    response_model=MenuReturn,
    status_code=status.HTTP_201_CREATED
)
def create_menu(data: MenuWrite, menu: MenuService = Depends()):
    return menu.create(data)


@router.get(
    '/{menu_id}',
    response_model=MenuRead,
    status_code=status.HTTP_200_OK
)
def get_menu(menu_id: UUID, menu: MenuService = Depends()):
    return menu.retrieve(menu_id)


@router.patch(
    '/{menu_id}',
    response_model=MenuReturn,
    status_code=status.HTTP_200_OK
)
def update_menu(menu_id: UUID, data: MenuWrite, menu: MenuService = Depends()):
    return menu.update(menu_id, data)


@router.delete('/{menu_id}', status_code=status.HTTP_200_OK)
def delete_menu(menu_id: UUID, menu: MenuService = Depends()):
    return menu.delete(menu_id)
