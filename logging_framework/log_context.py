import time
from typing import Dict, Any
from contextvars import ContextVar

# -------------------------------
# Context storage: per-request context map
# -------------------------------
# The ContextVar stores a dict: {request_id: LogContext}
_current_context: ContextVar[Dict[str, "LogContext"]] = ContextVar("log_context_map", default={})


class LogContext:
    """
    Stores request-scoped context data for logs and summary.
    """

    def __init__(self, request_id: str):
        self.request_id = request_id
        self.start_time = time.time()
        self.data: Dict[str, Any] = {}

    def add(self, key: str, value: Any):
        """Add a key-value pair to the context"""
        self.data[key] = value

    def summary(self) -> Dict[str, Any]:
        """Return a summary of the context"""
        return {
            "request_id": self.request_id,
            "total_pipeline_time": round(time.time() - self.start_time, 3),
            **self.data,
        }


# -------------------------------
# Context API
# -------------------------------
def set_context(ctx: LogContext):
    """
    Set the context for a specific request_id
    """
    context_map = _current_context.get()
    context_map[ctx.request_id] = ctx
    _current_context.set(context_map)


def get_context(request_id: str) -> LogContext | None:
    """
    Get context for a given request_id
    """
    context_map = _current_context.get()
    return context_map.get(request_id)


def add_to_context(request_id: str, key: str, value: Any):
    """
    Add a key-value pair to the context of a given request_id.
    Raises RuntimeError if context is not initialized.
    """
    ctx = get_context(request_id)
    if ctx is None:
        raise RuntimeError(f"Context not initialized for request_id={request_id}")
    ctx.add(key, value)