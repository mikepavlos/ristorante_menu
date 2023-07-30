from fastapi import APIRouter, HTTPException, status
from menu_app.menu.schemas import DishBase, DishRead
from menu_app.menu.models import Model, Submenu, Dish
from menu_app.database import db, engine
from uuid import UUID, uuid4

router = APIRouter()


@router.get(
    '/',
    response_model=list[DishRead],
    status_code=status.HTTP_200_OK
)
def get_all_dishes():
    dishes = db.query(Dish).all()

    # if dishes is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail='dishes not found'
    #     )

    return dishes


@router.post(
    '/',
    response_model=DishRead,
    status_code=status.HTTP_201_CREATED
)
def create_dish(submenu_id: UUID, dish: DishBase):
    submenu = db.query(Submenu).get(submenu_id)

    if submenu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'submenu with id {submenu_id} not found'
        )

    new_dish = Dish(
        id=uuid4(),
        title=dish.title,
        description=dish.description,
        price=dish.price,
        submenu_id=submenu_id
    )

    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)

    return new_dish


@router.get(
    '/{dish_id}',
    response_model=DishRead,
    status_code=status.HTTP_200_OK
)
def get_dish(dish_id: UUID):
    dish = db.query(Dish).get(dish_id)

    if dish is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dish not found'
        )

    # dish.price = dish.price

    return dish


@router.patch(
    '/{dish_id}',
    response_model=DishRead,
    status_code=status.HTTP_200_OK
)
def update_dish(dish_id: UUID, dish: DishBase):
    dish_update = db.query(Dish).get(dish_id)

    if dish_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dish not found'
        )

    dish_update.title = dish.title
    dish_update.description = dish.description
    dish_update.price = dish.price

    db.commit()
    db.refresh(dish_update)

    return dish_update


@router.delete('/{dish_id}', status_code=status.HTTP_200_OK)
def delete_dish(dish_id: UUID):
    dish_to_delete = db.query(Dish).get(dish_id)

    if dish_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dish not found'
        )

    db.delete(dish_to_delete)
    db.commit()

    return {
        'status': 'true',
        'message': 'The dish has been deleted'
    }
