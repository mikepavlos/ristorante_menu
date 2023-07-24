from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, status

from menu_app.database import db
from menu_app.menu.models import Menu, Submenu, Dish
from menu_app.menu.schemas import MenuBase, MenuRead

router = APIRouter()


@router.get(
    '/',
    response_model=list[MenuRead],
    status_code=status.HTTP_200_OK
)
def get_all_menus():
    menus = db.query(Menu).all()

    if menus is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menus not found'
        )

    for menu in menus:
        menu.submenus_count = db.query(
            Menu.id == Submenu.menu_id).count()

    return menus


@router.post(
    '/',
    response_model=MenuRead,
    status_code=status.HTTP_201_CREATED
)
def create_menu(menu: MenuBase):
    new_menu = Menu(
        id=uuid4(),
        title=menu.title,
        description=menu.description,
    )

    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)

    return new_menu


@router.get(
    '/{menu_id}',
    response_model=MenuRead,
    status_code=status.HTTP_200_OK
)
def get_menu(menu_id: UUID):
    menu = db.query(Menu).get(menu_id)

    if menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu not found'
        )

    menu.submenus_count = db.query(
        Submenu.menu_id == menu_id).count()

    menu.dishes_count = db.query(
        Dish.submenu_id == Submenu.id).where(
        Submenu.menu_id == menu_id).count()

    return menu


@router.patch(
    '/{menu_id}',
    response_model=MenuRead,
    status_code=status.HTTP_200_OK
)
def update_menu(menu_id: UUID, menu: MenuBase):
    menu_update = db.query(Menu).get(menu_id)

    if menu_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu not found'
        )

    menu_update.title = menu.title
    menu_update.description = menu.description

    db.commit()
    db.refresh(menu_update)

    return menu_update


@router.delete('/{menu_id}', status_code=status.HTTP_200_OK)
def delete_menu(menu_id: UUID):
    menu = db.query(Menu).get(menu_id)

    if menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu not found'
        )

    db.delete(menu)
    db.commit()

    return {
        'status': 'true',
        'message': 'The menu has been deleted'
    }
