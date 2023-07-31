from uuid import UUID

from fastapi import APIRouter, status

from menu_app.menu.schemas import SubmenuBase, SubmenuRead
from menu_app.menu.services.submenu import (
    submenu_list,
    submenu_create,
    submenu_obj,
    submenu_update,
    submenu_delete
)

router = APIRouter()


@router.get(
    '/',
    response_model=list[SubmenuRead],
    status_code=status.HTTP_200_OK
)
def get_all_submenus():
    return submenu_list()


@router.post(
    '/',
    response_model=SubmenuRead,
    status_code=status.HTTP_201_CREATED
)
def create_submenu(menu_id: UUID, submenu: SubmenuBase):
    return submenu_create(menu_id, submenu)


@router.get(
    '/{submenu_id}',
    response_model=SubmenuRead,
    status_code=status.HTTP_200_OK
)
def get_submenu(submenu_id: UUID):
    return submenu_obj(submenu_id)


@router.patch(
    '/{submenu_id}',
    response_model=SubmenuRead,
    status_code=status.HTTP_200_OK
)
def update_submenu(submenu_id: UUID, submenu: SubmenuBase):
    return submenu_update(submenu_id, submenu)


@router.delete('/{submenu_id}', status_code=status.HTTP_200_OK)
def delete_submenu(submenu_id: UUID):
    submenu_delete(submenu_id)

    return {
        'status': 'true',
        'message': 'The submenu has been deleted'
    }
