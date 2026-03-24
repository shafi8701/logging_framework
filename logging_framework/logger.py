import logging
import json
from datetime import datetime


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

        # -------------------------------
        # 🧠 Include exception info (important)
        # -------------------------------
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        # -------------------------------
        # 🧠 Standard attributes to ignore
        # -------------------------------
        standard_attrs = {
            "name", "msg", "args", "levelname", "levelno", "pathname",
            "filename", "module", "exc_info", "exc_text", "stack_info",
            "lineno", "funcName", "created", "msecs", "relativeCreated",
            "thread", "threadName", "processName", "process"
        }

        # -------------------------------
        # 🚀 Add dynamic extra fields
        # -------------------------------
        for key, value in record.__dict__.items():
            if key not in standard_attrs and key not in log_record:
                try:
                    json.dumps(value)  # ensure serializable
                    log_record[key] = value
                except Exception:
                    log_record[key] = str(value)

        return json.dumps(log_record)