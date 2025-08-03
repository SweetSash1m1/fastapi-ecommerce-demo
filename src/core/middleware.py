from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.monitoring import middlewares
from src.core.settings import settings


def register_middleware(app: FastAPI) -> None:
    for middleware in middlewares:
        app.add_middleware(middleware)
    app.add_middleware(CORSMiddleware, **settings.CORS.model_dump())
