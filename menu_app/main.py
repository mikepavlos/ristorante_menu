from fastapi import FastAPI
from starlette.responses import RedirectResponse

from menu_app.database import Model, engine
from menu_app.menu.routers import dishes, menus, submenus

Model.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def index():
    return RedirectResponse('docs')


app.include_router(
    menus.router,
    prefix="/api/v1/menus",
    tags=["menus"])

app.include_router(
    submenus.router,
    prefix="/api/v1/menus/{menu_id}/submenus",
    tags=["submenus"])

app.include_router(
    dishes.router,
    prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    tags=["dishes"])
