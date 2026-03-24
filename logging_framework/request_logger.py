# logging_framework/request_logger.py
import logging
from .log_context import get_context

class RequestLogger:
    """
    Logger wrapper:
    - Automatically attaches request_id to all logs.
    - Full context is only added for summary logs.
    """

    SUMMARY_LEVEL = 25  # Custom log level for summary

    def __init__(self, base_logger: logging.Logger):
        self.logger = base_logger
        logging.addLevelName(self.SUMMARY_LEVEL, "SUMMARY")

    def _log(self, level: str, message: str, extra: dict = None, **kwargs):
        """
        Normal logs include only request_id from current context.
        """
        user_extra = extra.copy() if extra else {}
        ctx = get_context()
        if ctx:
            user_extra["request_id"] = ctx.request_id

        log_method = getattr(self.logger, level)
        log_method(message, extra=user_extra, **kwargs)

    # Standard log levels
    def debug(self, message: str, extra=None, **kwargs):
        self._log("debug", message, extra=extra)

    def info(self, message: str, extra=None, **kwargs):
        self._log("info", message, extra=extra)

    def warning(self, message=None, extra=None, **kwargs):
        self._log("warning", message, extra=extra)

    def error(self, message: str, extra=None, **kwargs):
        self._log("error", message, extra=extra)

    def critical(self, message: str, extra=None, **kwargs):
        self._log("critical", message, extra=extra)

    def exception(self, message: str, extra=None, **kwargs):
        kwargs["exc_info"] = True
        self._log("error", message, extra=extra)

    # Summary logs include full context snapshot
    def summary(self, message: str, extra=None, **kwargs):
        user_extra = extra.copy() if extra else {}
        ctx = get_context()
        if ctx:
            user_extra["request_id"] = ctx.request_id
            user_extra.update(ctx.summary())
        self.logger.log(self.SUMMARY_LEVEL, message, extra=user_extra, **kwargs)