# logging_framework/__init__.py
import logging
import os
import yaml
from pathlib import Path
from logging.handlers import RotatingFileHandler

from .logger import JsonFormatter
from .request_logger import RequestLogger

# -------------------------------
# Base directory
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent

# -------------------------------
# Load Config
# -------------------------------
CONFIG_PATH = BASE_DIR / "config.yaml"
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

environment = os.getenv("ENV", "dev")
env_config = config.get(environment, {}).get("logging", {})

log_level_str = env_config.get("level", "INFO")
log_level = getattr(logging, log_level_str.upper(), logging.INFO)

rotation_config = env_config.get("rotation", {})
max_bytes = rotation_config.get("max_bytes", 10 * 1024 * 1024)
backup_count = rotation_config.get("backup_count", 5)

# -------------------------------
# Log folder
# -------------------------------
log_folder = Path(os.getenv("LOG_PATH", BASE_DIR / config["logging"]["folder"]))
log_folder.mkdir(parents=True, exist_ok=True)
log_file = log_folder / config["logging"]["file_name"]

# -------------------------------
# Formatter
# -------------------------------
json_formatter = JsonFormatter()

# -------------------------------
# File handler with rotation
# -------------------------------
file_handler = RotatingFileHandler(
    log_file,
    maxBytes=max_bytes,
    backupCount=backup_count,
)
file_handler.setFormatter(json_formatter)

# -------------------------------
# Console handler
# -------------------------------
console_handler = logging.StreamHandler()
console_handler.setFormatter(json_formatter)

# -------------------------------
# Logger setup
# -------------------------------
_logger = logging.getLogger(config.get("app_name", "app"))
_logger.setLevel(log_level)
_logger.addHandler(file_handler)
_logger.addHandler(console_handler)
_logger.propagate = False

# -------------------------------
# Public APIs
# -------------------------------
def get_logger() -> logging.Logger:
    return _logger

def get_request_logger() -> RequestLogger:
    """
    Returns a RequestLogger instance.
    Automatically reads request_id from current LogContext.
    """
    return RequestLogger(_logger)