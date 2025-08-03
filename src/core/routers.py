from fastapi import FastAPI

from src.core.healthcheck import router as healthcheck_router


def register_routers(app: FastAPI) -> None:
    app.include_router(healthcheck_router)
