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
- 🔹 **Docker-ready** — logs volume-mountable in containers.

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

## 🧩 Usage in Your Project / Downstream Flows

1. **Initialize a request context** in your entry point (e.g., `main.py`):

```python
from logging_framework import get_request_logger
from logging_framework.log_context import LogContext, set_context, add_to_context
import uuid

# Create a context for this request
ctx = LogContext()
ctx.set_request_id(str(uuid.uuid4()))
set_context(ctx)

# Get the logger (no arguments required)
logger = get_request_logger()

# Add contextual info for summary logs
add_to_context("user_id", 1234)
add_to_context("query", "SELECT * FROM table")
```

2. **Log messages in downstream modules or functions**:

```python
# downstream_module.py
from logging_framework import get_request_logger
from logging_framework.log_context import add_to_context

def process_data(records):
    logger = get_request_logger()  # automatically uses current request context
    logger.info("Starting data processing", extra={"record_count": len(records)})

    for i, record in enumerate(records):
        logger.debug(f"Processing record {i}")
    
    # Add info for summary logs
    add_to_context("records_processed", len(records))
    logger.info("Finished processing records")
```

3. **Log a summary at the end of your pipeline**:

```python
logger.summary("Pipeline Summary", extra={"component": "evaluation"})
```

- The **summary log** automatically includes:  
  - `request_id`  
  - All context data added via `add_to_context()`  
  - Total time since context creation (`total_pipeline_time`)  

4. **Key Points**:

- Normal logs (`debug`, `info`, `warning`, `error`, `critical`) automatically include `request_id`.  
- Only `summary()` includes the full context snapshot.  
- No need to pass `request_id` or context object to downstream modules.  
- `add_to_context()` is how you attach pipeline-specific metadata for the final summary log.

---

## 🔄 Log Rotation

- Triggered when file exceeds `max_bytes`.  
- Keeps up to `backup_count` rotated logs.  
- Prevents unbounded log growth.

---

