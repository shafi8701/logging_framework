FROM python:3.11-slim

WORKDIR /

# -------------------------------
# 📦 Install logging framework (local folder)
# -------------------------------
COPY logging_framework ./logging_framework
RUN pip install --no-cache-dir ./logging_framework

# -------------------------------
# 📦 Install other dependencies (if any)
# -------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -------------------------------
# 📁 Copy app code
# -------------------------------
COPY app/main.py .

# -------------------------------
# ⚙️ Env
# -------------------------------
ENV PYTHONUNBUFFERED=1

# Optional: override logs path
ENV LOG_PATH=/app/logs

# -------------------------------
# 🚀 Run
# -------------------------------
CMD ["python", "main.py"]