# logging_framework/log_context.py
import time
import contextvars
from typing import Dict, Any

# Thread/async-safe context
_current_context: contextvars.ContextVar["LogContext"] = contextvars.ContextVar("current_log_context", default=None)

class LogContext:
    """
    Stores request-scoped context data for logs and summary.
    """
    def __init__(self):
        self.request_id = str(time.time())  # default, overridden per request
        self.start_time = time.time()
        self.data: Dict[str, Any] = {}

    def set_request_id(self, request_id: str):
        self.request_id = request_id

    def add(self, key: str, value: Any):
        self.data[key] = value

    def summary(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "total_pipeline_time": round(time.time() - self.start_time, 3),
            **self.data,
        }

# -------------------------------
# Helpers for contextvars
# -------------------------------

def set_context(ctx: LogContext):
    """Set current context."""
    _current_context.set(ctx)

def get_context() -> LogContext:
    """Get current context. Returns None if not set."""
    return _current_context.get()

def add_to_context(key: str, value: Any):
    """Add key-value to current context."""
    ctx = get_context()
    if ctx is None:
        raise RuntimeError("LogContext not initialized for current request")
    ctx.add(key, value)