# logging_framework/request_logger.py
import logging
from .log_context import LogContext

class RequestLogger:
    """
    Logger wrapper that attaches request context and supports summary logs.
    """

    SUMMARY_LEVEL = 25  # Custom log level for summary

    def __init__(self, base_logger: logging.Logger, request_id: str, context: LogContext = None):
        self.logger = base_logger
        self.request_id = request_id
        self.context = context

        # Add summary level to logger
        logging.addLevelName(self.SUMMARY_LEVEL, "SUMMARY")

    def _log(self, level: str, message: str, extra: dict = None, **kwargs):
        user_extra = extra.copy() if extra else {}
        user_extra["request_id"] = self.request_id

        if self.context:
            user_extra.update(self.context.data)

        log_method = getattr(self.logger, level)
        log_method(message, extra=user_extra, **kwargs)

    def debug(self, message: str, extra=None, **kwargs):
        self._log("debug", message, extra=extra, **kwargs)

    def info(self, message: str, extra=None, **kwargs):
        self._log("info", message, extra=extra, **kwargs)

    def warning(self, message: str, extra=None, **kwargs):
        self._log("warning", message, extra=extra, **kwargs)

    def error(self, message: str, extra=None, **kwargs):
        self._log("error", message, extra=extra, **kwargs)

    def critical(self, message: str, extra=None, **kwargs):
        self._log("critical", message, extra=extra, **kwargs)

    def exception(self, message: str, extra=None, **kwargs):
        kwargs["exc_info"] = True
        self._log("error", message, extra=extra, **kwargs)

    def summary(self, message: str, extra=None, **kwargs):
        user_extra = extra.copy() if extra else {}
        user_extra["request_id"] = self.request_id
        if self.context:
            user_extra.update(self.context.data)
        self.logger.log(self.SUMMARY_LEVEL, message, extra=user_extra, **kwargs)