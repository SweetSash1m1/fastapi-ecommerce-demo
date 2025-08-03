import logging
from datetime import datetime, timezone
from typing import Any

from pythonjsonlogger.json import JsonFormatter

from src.core.enums import LoggerComponentEnum, LoggerNameEnum


class CustomJsonFormatter(JsonFormatter):
    def add_fields(
        self,
        log_record: dict[str, Any],
        record: logging.LogRecord,
        message_dict: dict[str, Any],
    ) -> None:
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            # this doesn't use record.created, so it is slightly off
            now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


# --------------- Configuring the global handler ---------------
_handler = logging.StreamHandler()
_formatter = CustomJsonFormatter("%(timestamp)s %(level)s %(name)s %(message)s")
_handler.setFormatter(_formatter)
_handler.setLevel(logging.INFO)


# --------------- Logger factory ---------------
def get_logger(name: str, component: str | None = None) -> logging.LoggerAdapter[Any]:
    """
    Get preconfigured logger by name.

    Returns a logger with the name 'name', which automatically uses the
    preconfigured handler and formatter.
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.addHandler(_handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
    extras = {"component": component} if component else {}
    return logging.LoggerAdapter(logger, extras)


# --------------- Implementations for specific purposes ---------------
def get_perf_logger() -> logging.LoggerAdapter[Any]:
    return get_logger(LoggerNameEnum.PERF_LOGGER, component=LoggerComponentEnum.PERF)


def get_access_logger() -> logging.LoggerAdapter[Any]:
    return get_logger(LoggerNameEnum.ACCESS_LOGGER, component=LoggerComponentEnum.ACCESS)


def get_security_logger() -> logging.LoggerAdapter[Any]:
    return get_logger(
        LoggerNameEnum.SECURITY_LOGGER, component=LoggerComponentEnum.SECURITY
    )


def get_error_logger() -> logging.LoggerAdapter[Any]:
    return get_logger(LoggerNameEnum.ERRORS_LOGGER, component=LoggerComponentEnum.ERRORS)


def get_app_logger() -> logging.LoggerAdapter[Any]:
    return get_logger(
        LoggerNameEnum.APPLICATION_LOGGER, component=LoggerComponentEnum.APPLICATION
    )
