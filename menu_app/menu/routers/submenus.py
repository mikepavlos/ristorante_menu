from fastapi import APIRouter, HTTPException, status
from menu_app.menu.schemas import SubmenuBase, SubmenuRead
from menu_app.menu.models import Model, Menu, Submenu, Dish
from menu_app.database import db, engine
from uuid import UUID, uuid4

router = APIRouter()


@router.get(
    '/',
    response_model=list[SubmenuRead],
    status_code=status.HTTP_200_OK
)
def get_all_submenus():
    submenus = db.query(Submenu).all()

    if submenus is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenus not found'
        )

    return submenus


@router.post(
    '/',
    response_model=SubmenuRead,
    status_code=status.HTTP_201_CREATED
)
def create_submenu(menu_id: UUID, submenu: SubmenuBase):
    menu = db.query(Menu).get(menu_id)

    if menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'menu with id {menu_id} not found'
        )

    new_submenu = Submenu(
        id=uuid4(),
        title=submenu.title,
        description=submenu.description,
        menu_id=menu_id
    )

    db.add(new_submenu)
    db.commit()
    db.refresh(new_submenu)

    return new_submenu


@router.get(
    '/{submenu_id}',
    response_model=SubmenuRead,
    status_code=status.HTTP_200_OK
)
def get_submenu(submenu_id: UUID):
    submenu = db.query(Submenu).get(submenu_id)

    if submenu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu not found'
        )

    submenu.dishes_count = db.query(
        Dish.submenu_id ==
        Submenu.id).count()

    return submenu


@router.patch(
    '/{submenu_id}',
    response_model=SubmenuRead,
    status_code=status.HTTP_200_OK
)
def update_submenu(submenu_id: UUID, submenu: SubmenuBase):
    submenu_update = db.query(Submenu).get(submenu_id)

    if submenu_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu not found'
        )

    submenu_update.title = submenu.title
    submenu_update.description = submenu.description

    db.commit()
    db.refresh(submenu_update)

    return submenu_update


@router.delete('/{submenu_id}', status_code=status.HTTP_200_OK)
def delete_submenu(submenu_id: UUID):
    submenu_delete = db.query(Submenu).get(submenu_id)

    if submenu_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu not found'
        )

    db.delete(submenu_delete)
    db.commit()

    return {
        'status': 'true',
        'message': 'The submenu has been deleted'
    }
