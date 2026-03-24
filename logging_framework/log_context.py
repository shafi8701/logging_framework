# logging_framework/log_context.py
import time
from typing import Dict, Any

class LogContext:
    """
    Stores request-scoped context data for logs and summary.
    """

    _contexts: Dict[str, "LogContext"] = {}

    @classmethod
    def get_context(cls, request_id: str) -> "LogContext":
        return cls._contexts.get(request_id)

    @classmethod
    def set_context(cls, request_id: str, ctx: "LogContext"):
        cls._contexts[request_id] = ctx

    def __init__(self, request_id: str):
        self.request_id = request_id
        self.start_time = time.time()
        self.data: Dict[str, Any] = {}

    def add(self, key: str, value: Any):
        self.data[key] = value

    def summary(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "total_pipeline_time": round(time.time() - self.start_time, 3),
            **self.data,
        }


# -------------------------------
# Optional helpers for convenience
# -------------------------------

def set_context(request_id: str, ctx: LogContext):
    LogContext.set_context(request_id, ctx)

def get_context(request_id: str) -> LogContext:
    return LogContext.get_context(request_id)

def add_to_context(request_id: str, key: str, value: Any):
    ctx = LogContext.get_context(request_id)
    if ctx is None:
        raise RuntimeError(f"Context for request_id={request_id} not initialized")
    ctx.add(key, value)