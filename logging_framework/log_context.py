import time
from contextvars import ContextVar
from typing import Dict, Any

_current_context: ContextVar = ContextVar("log_context", default=None)

class LogContext:
    def __init__(self, request_id: str):
        self.request_id = request_id
        self.start_time = time.time()
        self.data: Dict[str, Any] = {}

    def add(self, key: str, value: Any):
        self.data[key] = value

    def summary(self):
        return {
            "request_id": self.request_id,
            "total_pipeline_time": round(time.time() - self.start_time, 3),
            **self.data,
        }

def set_context(ctx: LogContext):
    _current_context.set(ctx)

def get_context() -> LogContext | None:
    return _current_context.get()

def add_to_context(key: str, value: Any):
    ctx = _current_context.get()
    if ctx is None:
        raise RuntimeError("Context not initialized")
    ctx.add(key, value)