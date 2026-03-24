import yaml
import logging
import os
from pathlib import Path
from queue import Queue
from logging.handlers import QueueHandler, QueueListener, RotatingFileHandler

from .logger import JsonFormatter
from .request_logger import RequestLogger

# -------------------------------
# 📁 Base directory (this module)
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent

# -------------------------------
# 📄 Load Config
# -------------------------------
CONFIG_PATH = BASE_DIR / "config.yaml"

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

# -------------------------------
# 🌍 Environment Setup
# -------------------------------
environment = config["environment"]
env_config = config.get(environment, {}).get("logging", {})

log_level_str = env_config.get("level", "INFO")
log_level = getattr(logging, log_level_str.upper(), logging.INFO)

app_name = config.get("app_name", "app")

# -------------------------------
# 📁 Log Folder (ENV override)
# -------------------------------
# Priority:
# 1. LOG_PATH env variable
# 2. config.yaml folder
# -------------------------------
env_log_path = os.getenv("LOG_PATH")

if env_log_path:
    log_folder = Path(env_log_path)
else:
    log_folder = BASE_DIR / config["logging"]["folder"]

log_folder.mkdir(parents=True, exist_ok=True)

# -------------------------------
# 📄 Log Files
# -------------------------------
log_file = log_folder / config["logging"]["file_name"]
log_file_summary = log_folder / config["logging"]["file_name_summary"]

# -------------------------------
# 🔄 Rotation Config (Size-based)
# -------------------------------
rotation_config = env_config.get("rotation", {})

max_bytes = rotation_config.get("max_bytes", 10 * 1024 * 1024)
backup_count = max(1, rotation_config.get("backup_count", 5))

# -------------------------------
# 🎨 Formatter
# -------------------------------
json_formatter = JsonFormatter()

# -------------------------------
# 📁 Handlers (Size rotation + auto purge)
# -------------------------------
file_handler = RotatingFileHandler(
    log_file,
    maxBytes=max_bytes,
    backupCount=backup_count
)
file_handler.setFormatter(json_formatter)

summary_handler = RotatingFileHandler(
    log_file_summary,
    maxBytes=max_bytes // 2,
    backupCount=max(1, backup_count // 2)
)
summary_handler.setFormatter(json_formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(json_formatter)

# -------------------------------
# ⚡ Async Logging Setup
# -------------------------------
log_queue = Queue(-1)
queue_handler = QueueHandler(log_queue)

queue_listener = QueueListener(
    log_queue,
    file_handler,
    summary_handler,
    console_handler,
    respect_handler_level=True
)

# -------------------------------
# 🪵 Logger Singleton
# -------------------------------
_logger = logging.getLogger(app_name)

if not _logger.handlers:
    _logger.setLevel(log_level)
    _logger.addHandler(queue_handler)
    _logger.propagate = False

    queue_listener.start()

# -------------------------------
# 🎯 Public APIs
# -------------------------------
def get_logger():
    return _logger


def get_request_logger(request_id: str) -> RequestLogger:
    return RequestLogger(_logger, request_id)