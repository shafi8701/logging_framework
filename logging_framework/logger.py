# logging_framework/logger.py
import logging
import json
from datetime import datetime

class JsonFormatter(logging.Formatter):
    """
    Formats logs in structured JSON.
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

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        # Include extra fields
        standard_attrs = {
            "name", "msg", "args", "levelname", "levelno", "pathname",
            "filename", "module", "exc_info", "exc_text", "stack_info",
            "lineno", "funcName", "created", "msecs", "relativeCreated",
            "thread", "threadName", "processName", "process"
        }

        for key, value in record.__dict__.items():
            if key not in standard_attrs and key not in log_record:
                try:
                    json.dumps(value)
                    log_record[key] = value
                except Exception:
                    log_record[key] = str(value)

        return json.dumps(log_record)