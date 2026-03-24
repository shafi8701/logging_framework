import logging
from .log_context import LogContext

# -------------------------------
# Custom SUMMARY level
# -------------------------------
SUMMARY_LEVEL = 25
logging.addLevelName(SUMMARY_LEVEL, "SUMMARY")


class RequestLogger:
    """
    Request-scoped logger wrapper.
    - Injects request_id into all logs
    - Supports a separate summary method
    """

    def __init__(self, base_logger: logging.Logger, request_id: str, context: LogContext = None):
        self.logger = base_logger
        self.request_id = request_id
        self.context = context

    def _log(self, level: str, message: str, extra: dict = None, **kwargs):
        """
        Centralized logging method.
        Automatically injects request_id and context data.
        """
        user_extra = extra.copy() if extra else {}
        user_extra["request_id"] = self.request_id

        # Inject context data if available
        if self.context:
            user_extra.update(self.context.data)

        # Get the logging method dynamically
        log_method = getattr(self.logger, level)
        log_method(message, extra=user_extra, **kwargs)

    # -------------------------------
    # Standard logging methods
    # -------------------------------
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

    # -------------------------------
    # Special SUMMARY log method
    # -------------------------------
    def summary(self, message: str, extra=None, **kwargs):
        """
        Logs at custom SUMMARY level.
        Will appear in the single log file alongside other logs.
        """
        user_extra = extra.copy() if extra else {}
        user_extra["request_id"] = self.request_id
        if self.context:
            user_extra.update(self.context.data)

        self.logger.log(SUMMARY_LEVEL, message, extra=user_extra, **kwargs)