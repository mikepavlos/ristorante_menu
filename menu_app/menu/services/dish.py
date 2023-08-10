# from uuid import uuid4
#
# from menu_app.menu import crud
# from menu_app.menu.cache_repository import clear_cache, get_cache, set_cache
# from menu_app.menu.models import Dish, Submenu
#
#
# def dish_list():
#     if dish_cache := get_cache('dish:list'):
#         return dish_cache
#
#     dishes = crud.db_all(Dish)
#     set_cache('dish:list', dishes)
#     return dishes
#
#
# def dish_obj(dish_id):
#     if dish_cache := get_cache(f'dish:{dish_id}'):
#         return dish_cache
#
#     dish = crud.get(Dish, dish_id, 'dish')
#     set_cache(f'dish:{dish_id}', dish)
#     return dish
#
#
# def dish_create(submenu_id, data):
#     crud.get(Submenu, submenu_id, 'submenu')
#     dish = Dish(
#         id=uuid4(),
#         title=data.title,
#         description=data.description,
#         price=data.price,
#         submenu_id=submenu_id
#     )
#     crud.db_create(dish)
#
#     set_cache(f'dish:{dish.id}', dish)
#     clear_cache('dish:list')
#     clear_cache(f'submenu:{submenu_id}')
#     clear_cache('submenu:list')
#     clear_cache(f'menu:{dish.submenu.menu_id}')
#     clear_cache('menu:list')
#
#     return dish
#
#
# def dish_update(dish_id, data):
#     dish = crud.get(Dish, dish_id, 'dish')
#     dish.title = data.title
#     dish.description = data.description
#     dish.price = data.price
#     crud.db_update(dish)
#
#     set_cache(f'dish:{dish.id}', dish)
#     clear_cache('dish:list')
#
#     return dish
#
#
# def dish_delete(dish_id):
#     dish = crud.get(Dish, dish_id, 'dish')
#     crud.db_delete(dish)
#
#     clear_cache(f'dish:{dish.id}')
#     clear_cache('dish:list')
#     clear_cache(f'submenu:{dish.submenu_id}')
#     clear_cache('submenu:list')
#     clear_cache(f'menu:{dish.submenu.menu_id}')
#     clear_cache('menu:list')
