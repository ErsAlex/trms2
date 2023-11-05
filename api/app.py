from fastapi import FastAPI
from .routers import all_routers


def create_app():
    app = FastAPI(
        debug=True,
        docs_url="/api/docs",
        title="FastApi Task Rooms"
        )
    for router in all_routers:
        app.include_router(router)
    return app


