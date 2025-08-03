from enum import StrEnum

from src.core.settings import settings


class LogTypeEnum(StrEnum):
    API_REQUEST = "API_REQUEST"
    API_RESPONSE = "API_RESPONSE"
    DB = "DB"


class LoggerNameEnum(StrEnum):
    PERF_LOGGER = f"{settings.APP_NAME}.perf"
    ACCESS_LOGGER = f"{settings.APP_NAME}.access"
    SECURITY_LOGGER = f"{settings.APP_NAME}.security"
    ERRORS_LOGGER = f"{settings.APP_NAME}.errors"
    APPLICATION_LOGGER = f"{settings.APP_NAME}.application"


class LoggerComponentEnum(StrEnum):
    PERF = "perf"
    ACCESS = "access"
    SECURITY = "security"
    ERRORS = "errors"
    APPLICATION = "application"
