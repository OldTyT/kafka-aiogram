"""Logging."""

import logging
import os
import sys

from loguru import logger  # noqa: F811


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        logging.CRITICAL: "CRITICAL",
        logging.ERROR: "ERROR",
        logging.WARNING: "WARNING",
        logging.INFO: "INFO",
        logging.DEBUG: "DEBUG",
        logging.NOTSET: "NOTSET",
    }

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id="app")
        log.opt(depth=depth, colors=True, exception=record.exc_info).log(
            level, record.getMessage()
        )


def formatter(record):  # noqa: U100
    return (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>"
        " <level>{level}</level> <cyan>{name}:{function}:{line}</cyan>"
        " - <level>{message}</level>\n"
    )


class CustomizeLogger:
    @classmethod
    def customize_logging(cls):
        logger.remove()
        log_is_json = os.getenv("LOG_JSON", "")
        log_is_json = log_is_json.lower() in [
            "true",
            "1",
            "t",
            "y",
            "yes",
            "yeah",
            "yup",
            "certainly",
            "uh-huh",
        ]
        logger.add(
            sys.stderr,
            enqueue=True,
            backtrace=True,
            colorize=True,
            level=os.getenv("LOG_LEVEL", "INFO").upper(),
            format=formatter,
            serialize=log_is_json,
        )
        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        # logging.basicConfig(handlers=[InterceptHandler()])
        for _log in [
            # "aiogram",
            "asyncio",
        ]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return logger.bind(request_id=None, method=None)


logger = CustomizeLogger.customize_logging()  # noqa: F811
