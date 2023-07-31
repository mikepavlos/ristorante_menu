from fastapi import HTTPException
from starlette import status

from menu_app.database import db


def db_all(model):
    return db.query(model).all()


def db_get_or_404(model, obj_id, obj_name=''):
    obj = db.query(model).get(obj_id)

    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{obj_name} not found'
        )

    return obj


def db_create(obj):
    db.add(obj)
    db.commit()
    db.refresh(obj)


def db_update(obj):
    db.commit()
    db.refresh(obj)


def db_delete(obj):
    db.delete(obj)
    db.commit()
