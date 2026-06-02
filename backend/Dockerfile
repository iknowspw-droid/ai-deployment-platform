# ==========================================
# STAGE 1: The Builder
# ==========================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies needed for compiling certain python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only the dependency requirements file first to utilize Docker layer caching
COPY requirements.txt .

# Install dependencies into a localized custom directory (/install)
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ==========================================
# STAGE 2: The Final Runtime Environment
# ==========================================
FROM python:3.11-slim AS runner

WORKDIR /app

# Copy ONLY the pre-installed dependencies from the builder stage
COPY --from=builder /install /usr/local

# Copy our actual application code
COPY app.py .

# Security Best Practice: Run as a non-root user. 
# Root containers can be exploited to break out into the host system.
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Run Uvicorn asynchronously on port 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
