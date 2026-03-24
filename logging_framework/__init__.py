import logging
import os
from pathlib import Path
from queue import Queue
from logging.handlers import QueueHandler, QueueListener, RotatingFileHandler
from .logger import JsonFormatter
from .request_logger import RequestLogger

# -------------------------------
# Paths & Environment
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent
log_folder = Path(os.getenv("LOG_PATH", BASE_DIR / "logs"))
log_folder.mkdir(parents=True, exist_ok=True)
log_file = log_folder / "app.log"

# -------------------------------
# Custom SUMMARY level
# -------------------------------
SUMMARY_LEVEL = 25
logging.addLevelName(SUMMARY_LEVEL, "SUMMARY")

# -------------------------------
# Formatter
# -------------------------------
formatter = JsonFormatter()

# -------------------------------
# File handler
# -------------------------------
file_handler = RotatingFileHandler(
    log_file,
    maxBytes=10 * 1024 * 1024,
    backupCount=5
)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)  # everything INFO+ will go here

# -------------------------------
# Console handler (optional)
# -------------------------------
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.INFO)

# -------------------------------
# Async Logging
# -------------------------------
log_queue = Queue(-1)
queue_handler = QueueHandler(log_queue)
queue_listener = QueueListener(
    log_queue,
    file_handler,
    console_handler,
    respect_handler_level=True
)
queue_listener.start()

# -------------------------------
# Logger singleton
# -------------------------------
_logger = logging.getLogger("my_app")
if not _logger.handlers:
    _logger.setLevel(logging.INFO)
    _logger.addHandler(queue_handler)
    _logger.propagate = False

# -------------------------------
# Public API
# -------------------------------
def get_logger():
    return _logger

def get_request_logger(request_id: str, context=None) -> RequestLogger:
    return RequestLogger(_logger, request_id, context=context)