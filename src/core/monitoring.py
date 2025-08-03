import time
from typing import Awaitable, Callable

from fastapi.requests import Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.enums import LogTypeEnum
from src.core.logger import get_app_logger, get_perf_logger

app_logger = get_app_logger()
perf_logger = get_perf_logger()


class ExceptionsMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        try:
            return await call_next(request)
        except Exception as e:
            app_logger.error(
                "Exception",
                extra={
                    "error": str(e),
                    "path": request.url.path,
                    "method": request.method,
                    "user_agent": request.headers.get("User-Agent"),
                    "user_ip": request.headers.get("X-Forwarded-For"),
                },
                exc_info=True,
            )
            raise e


class PerfMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:

        start = time.perf_counter()
        response = await call_next(request)
        duration = (time.perf_counter() - start) * 1000

        perf_logger.info(
            {
                "type": LogTypeEnum.API_RESPONSE,
                "duration_ms": duration,
                "path": request.url.path,
                "user_agent": request.headers.get("User-Agent"),
                "user_ip": request.headers.get("X-Forwarded-For"),
            }
        )

        return response


# TODO what about user_id?!
class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:

        request_log_dict = {
            "type": LogTypeEnum.API_REQUEST,
            "url": request.url.path,
            "method": request.method,
            "user_agent": request.headers.get("User-Agent"),
            "user_ip": request.headers.get("X-Forwarded-For"),
        }
        app_logger.info(request_log_dict)

        response = await call_next(request)

        response_log_dict = {
            "type": LogTypeEnum.API_RESPONSE,
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "user_agent": request.headers.get("User-Agent"),
            "user_ip": request.headers.get("X-Forwarded-For"),
        }
        app_logger.info(response_log_dict)

        return response


middlewares = [
    ExceptionsMiddleware,
    PerfMiddleware,
    LogMiddleware,
]
