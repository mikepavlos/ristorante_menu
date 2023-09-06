from uuid import UUID

from fastapi import APIRouter, Depends, status

from menu_app.menu.menu_services import SubmenuService
from menu_app.menu.schemas import SubmenuRead, SubmenuReturn, SubmenuWrite

router = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus',
    tags=['submenus']
)


@router.get(
    '/',
    response_model=list[SubmenuRead],
    status_code=status.HTTP_200_OK
)
def get_all_submenus(
    submenu: SubmenuService = Depends()
):
    return submenu.list()


@router.post(
    '/',
    response_model=SubmenuReturn,
    status_code=status.HTTP_201_CREATED
)
def create_submenu(
    menu_id: UUID,
    data: SubmenuWrite,
    submenu: SubmenuService = Depends()
):
    return submenu.create(menu_id, data)


@router.get(
    '/{submenu_id}',
    response_model=SubmenuRead,
    status_code=status.HTTP_200_OK
)
def get_submenu(
    submenu_id: UUID,
    submenu: SubmenuService = Depends()
):
    return submenu.retrieve(submenu_id)


@router.patch(
    '/{submenu_id}',
    response_model=SubmenuReturn,
    status_code=status.HTTP_200_OK
)
def update_submenu(
    submenu_id: UUID,
    data: SubmenuWrite,
    submenu: SubmenuService = Depends()
):
    return submenu.update(submenu_id, data)


@router.delete(
    '/{submenu_id}',
    status_code=status.HTTP_200_OK
)
def delete_submenu(
    submenu_id: UUID,
    submenu: SubmenuService = Depends()
):
    return submenu.delete(submenu_id)
