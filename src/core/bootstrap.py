from fastapi import FastAPI

from src.core.lifespan import lifespan
from src.core.middleware import register_middleware
from src.core.routers import register_routers


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    register_routers(app)
    register_middleware(app)
    return app
