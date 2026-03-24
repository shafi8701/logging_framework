# Logging Framework

A Python **structured logging framework** with request-scoped context, JSON-formatted logs, summary logging, and automatic log rotation.  
Designed for easy integration into any Python project.

---

## Features

- ✅ **Structured JSON logs** with `timestamp`, `level`, `logger`, `module`, `function`, `line`, and `request_id`.
- ✅ **Request-scoped logging** with unique `request_id` per request.
- ✅ **Context support**: store extra information per request and automatically attach to all logs.
- ✅ **Summary logging**: special logs for pipeline summaries (e.g., RAG evaluations, metrics) with context data.
- ✅ **Log rotation & retention**: automatically rotates logs based on file size, keeps backup files.
- ✅ **Single log file**: all logs, including summary, go to the same file for simplicity.
- ✅ **Console output**: optional JSON-formatted console logs for visibility during development.
- ✅ **Docker-ready**: ready to run with volume-mounted log folder.

---

## Folder Structure
logging_framework/
├── init.py # Logger initialization & public APIs
├── logger.py # JSON formatter
├── request_logger.py # Request-scoped logger wrapper
├── log_context.py # Request context storage
├── config.yaml # Logging configuration
└── main.py # Example usage


---

## Configuration (`config.yaml`)

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
  folder: logs             # relative to this module
  file_name: app.json

app_name: my_app

Note:
1. dev and prod define environment-specific logging levels and rotation.
2. LOG_PATH environment variable overrides the log folder.
3. app_name defines the logger name.

Quick Start
1. Clone the repository
git clone <repo_url>
cd logging_framework
2. Build Docker image
docker build -t logging-framework:1.0 .
3. Run the example
docker run -e LOG_PATH=/app/logs -v $(pwd)/logs:/app/logs logging-framework:1.0
Logs will be written to logs/app.json.
Rotated logs are automatically created when max_bytes is exceeded.
All logs, including summary logs, are in a single file.
Example Output
{
  "timestamp": "2026-03-24T13:37:06.177040",
  "level": "INFO",
  "message": "Context initialized",
  "logger": "my_app",
  "module": "request_logger",
  "function": "_log",
  "line": 37,
  "request_id": "bfa58fbc-89ac-44ba-ba8a-903da7e11d60",
  "query": "Test Query",
  "query_length": 1
}
{
  "timestamp": "2026-03-24T13:37:06.272498",
  "level": "SUMMARY",
  "message": "RAG Summary",
  "logger": "my_app",
  "module": "request_logger",
  "function": "summary",
  "line": 68,
  "request_id": "bfa58fbc-89ac-44ba-ba8a-903da7e11d60",
  "component": "evaluation",
  "query": "Test Query",
  "query_length": 1,
  "total_pipeline_time": 0.095
}
Usage in Your Project
from logging_framework import get_request_logger
from logging_framework.log_context import LogContext

# Create a unique request ID per request
request_id = "unique-request-id"
ctx = LogContext(request_id)

# Initialize request-scoped logger
logger = get_request_logger(request_id, ctx)

# Add context data
ctx.add("user_id", 1234)

# Log normally
logger.info("Processing started")

# Log summary at end of request
logger.summary("Pipeline Summary", extra={"component": "evaluation"})
All logs automatically include request_id and context data.
Summary logs use SUMMARY level internally.
Log Rotation
Configured per environment in config.yaml.
Rotation occurs when log file exceeds max_bytes.
Keeps backup_count rotated files.
Ensures logs don’t grow indefinitely in production.
License

MIT License. Free to use, modify, and integrate into your projects.


---

If you want, I can also **update the Dockerfile and main.py comments** so that **any other developer can just clone the repo, build Docker, and see the logs with context and summary automatically**.  

Do you want me to do that next?
