
# 🚀 Python Structured Logging Framework

A lightweight, extensible **Python structured logging framework** featuring:

- JSON‑formatted logs  
- Request‑scoped context  
- Summary‑level metrics logging  
- Automatic log rotation  
- Console logging for local dev  
- Docker‑ready deployment  

Perfect for modern API services, RAG pipelines, microservices, and any Python project requiring reliable JSON logs.

---

## ✨ Features

- 🔹 **Structured JSON logs** including:  
  `timestamp`, `level`, `message`, `logger`, `module`, `function`, `line`, `request_id`, and context values.
- 🔹 **Request‑scoped logging** using a unique `request_id` per request.
- 🔹 **Context handling** — attach metadata automatically to every log entry.
- 🔹 **Summary logs** for pipeline‑level metrics (RAG results, evaluations, processing time, etc.).
- 🔹 **Log rotation** (size‑based) with configurable retention.
- 🔹 **Unified log file** — all logs (info, error, summary) stored together.
- 🔹 **Optional console JSON output** for development.
- 🔹 **Docker-ready** — logs volume‑mountable in containers.

---

## 📁 Project Structure

```
logging_framework/
├── __init__.py           # Logger initialization & public API
├── logger.py             # JSON log formatter
├── request_logger.py     # Request-scoped logging wrapper
├── log_context.py        # Context storage per request
├── config.yaml           # Logging configuration (dev/prod)
└── main.py               # Example usage
```

---

## ⚙️ Configuration (`config.yaml`)

```yaml
dev:
  logging:
    level: DEBUG
    rotation:
      max_bytes: 1048576   # 1MB per file
      backup_count: 2

prod:
  logging:
    level: WARNING
    rotation:
      max_bytes: 10485760  # 10MB per file
      backup_count: 5

logging:
  folder: logs             # relative path
  file_name: app.json

app_name: my_app
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone <repo_url>
cd logging_framework
```

### 2. Build Docker image

```bash
docker build -t logging-framework:1.0 .
```

### 3. Run the example

```bash
docker run   -e LOG_PATH=/app/logs   -v $(pwd)/logs:/app/logs   logging-framework:1.0
```

Logs will appear in `logs/app.json`.

---

## 📌 Example Output

(Example JSON omitted for brevity — see full README in chat above.)

---

## 🧩 Usage in Your Project

```python
from logging_framework import get_request_logger
from logging_framework.log_context import LogContext

request_id = "unique-request-id"
ctx = LogContext(request_id)
logger = get_request_logger(request_id, ctx)

ctx.add("user_id", 1234)
logger.info("Processing started")
logger.summary("Pipeline Summary", extra={"component": "evaluation"})
```

---

## 🔄 Log Rotation

- Triggered when file exceeds `max_bytes`.
- Keeps up to `backup_count` rotated logs.
- Prevents unbounded log growth.

---

MIT License

