class RequestLogger:
    """
    Request-scoped logger wrapper.
    - Injects request_id into all logs
    - Safely merges extra fields
    - Supports standard logging kwargs (exc_info, stack_info, etc.)
    """

    def __init__(self, base_logger, request_id: str, trace_id: str = None):
        self.logger = base_logger
        self.request_id = request_id
        self.trace_id = trace_id  # optional (future: distributed tracing)

    def _log(self, level: str, message: str, **kwargs):
        """
        Centralized safe logging handler.
        """

        # -------------------------------
        # 🔒 Extract and validate extra
        # -------------------------------
        user_extra = kwargs.pop("extra", {})

        if user_extra is None:
            user_extra = {}

        if not isinstance(user_extra, dict):
            raise ValueError("extra must be a dictionary")

        # -------------------------------
        # 🚫 Prevent override of core fields
        # -------------------------------
        protected_keys = {"request_id", "trace_id"}

        for key in protected_keys:
            if key in user_extra:
                user_extra.pop(key)

        # -------------------------------
        # 🔗 Merge system + user fields
        # -------------------------------
        merged_extra = {
            **user_extra,
            "request_id": self.request_id
        }

        if self.trace_id:
            merged_extra["trace_id"] = self.trace_id

        # -------------------------------
        # 📣 Get logging method safely
        # -------------------------------
        log_method = getattr(self.logger, level, None)

        if not log_method:
            raise ValueError(f"Invalid log level: {level}")

        # -------------------------------
        # 🚀 Emit log
        # -------------------------------
        log_method(
            message,
            extra=merged_extra,
            stacklevel=2,
            **kwargs
        )

    # -------------------------------
    # 🎯 Public methods
    # -------------------------------
    def debug(self, message: str, **kwargs):
        self._log("debug", message, **kwargs)

    def info(self, message: str, **kwargs):
        self._log("info", message, **kwargs)

    def warning(self, message: str, **kwargs):
        self._log("warning", message, **kwargs)

    def error(self, message: str, **kwargs):
        self._log("error", message, **kwargs)

    def critical(self, message: str, **kwargs):
        self._log("critical", message, **kwargs)

    def exception(self, message: str, **kwargs):
        """
        Convenience method for exception logging.
        Automatically includes stack trace.
        """
        kwargs["exc_info"] = True
        self._log("error", message, **kwargs)