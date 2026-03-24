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
