from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: int
    message: str


router = APIRouter(
    prefix="/health",
    tags=["Healthcheck"],
    responses={200: {"description": "Service is running"}},
)


@router.get("/", response_model=HealthResponse, summary="Check service health")
async def healthcheck() -> JSONResponse:
    return JSONResponse(content={"status": "ok", "message": "service is running"})
