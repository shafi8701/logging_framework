import logging
import json
from datetime import datetime

# -------------------------------
# Custom SUMMARY level
# -------------------------------
SUMMARY_LEVEL = 25
logging.addLevelName(SUMMARY_LEVEL, "SUMMARY")


class JsonFormatter(logging.Formatter):
    """
    Structured JSON formatter for logs.
    - Adds standard fields
    - Dynamically includes `extra` fields
    - Handles exceptions cleanly
    """

    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Include exception info if present
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        # Standard attributes to ignore when adding `extra`
        standard_attrs = {
            "name", "msg", "args", "levelname", "levelno", "pathname",
            "filename", "module", "exc_info", "exc_text", "stack_info",
            "lineno", "funcName", "created", "msecs", "relativeCreated",
            "thread", "threadName", "processName", "process"
        }

        # Include all extra fields dynamically
        for key, value in record.__dict__.items():
            if key not in standard_attrs and key not in log_record:
                try:
                    json.dumps(value)  # ensure serializable
                    log_record[key] = value
                except Exception:
                    log_record[key] = str(value)

        return json.dumps(log_record)


# -------------------------------
# Optional helper for SUMMARY logging
# -------------------------------
def log_summary(logger: logging.Logger, message: str, extra=None, **kwargs):
    """
    Convenience method to log at SUMMARY level directly.
    """
    user_extra = extra.copy() if extra else {}
    logger.log(SUMMARY_LEVEL, message, extra=user_extra, **kwargs)