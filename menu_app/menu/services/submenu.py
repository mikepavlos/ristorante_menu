# from uuid import uuid4
#
# from menu_app.menu import crud
# from menu_app.menu.cache_repository import clear_cache, get_cache, set_cache
# from menu_app.menu.models import Menu, Submenu
# from menu_app.menu.services.base import dishes_count


# def submenu_list():
#     if submenu_cache := get_cache('submenu:list'):
#         return submenu_cache
#
#     submenus = crud.db_all(Submenu)
#     for submenu in submenus:
#         submenu.dishes_count = dishes_count()
#
#     set_cache('submenu:list', submenus)
#
#     return submenus


# def submenu_obj(submenu_id):
#     if submenu_cache := get_cache(f'submenu:{submenu_id}'):
#         return submenu_cache
#
#     submenu = crud.get(Submenu, submenu_id, 'submenu')
#     submenu.dishes_count = dishes_count()
#
#     set_cache(f'submenu:{submenu_id}', submenu)
#
#     return submenu


# def submenu_create(menu_id, data):
#     crud.get(Menu, menu_id, 'menu')
#     submenu = Submenu(
#         id=uuid4(),
#         title=data.title,
#         description=data.description,
#         menu_id=menu_id
#     )
#     crud.db_create(submenu)
#
#     set_cache(f'submenu:{submenu.id}', submenu)
#     clear_cache('submenu:list')
#     clear_cache(f'menu:{menu_id}')
#     clear_cache('menu:list')
#
#     return submenu
#
#
# def submenu_update(submenu_id, data):
#     submenu = crud.get(Submenu, submenu_id, 'submenu')
#     submenu.title = data.title
#     submenu.description = data.description
#     submenu.dishes_count = dishes_count()
#     crud.db_update(submenu)
#
#     set_cache(f'submenu:{submenu_id}', submenu)
#     clear_cache('submenu:list')
#
#     return submenu
#
#
# def submenu_delete(submenu_id):
#     submenu = crud.get(Submenu, submenu_id, 'submenu')
#     crud.db_delete(submenu)
#
#     clear_cache(f'submenu:{submenu_id}')
#     clear_cache('submenu:list')
#     clear_cache(f'menu:{submenu.menu_id}')
#     clear_cache('menu:list')
