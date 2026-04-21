FROM python:3.13-slim

# Prevents Python from writing .pyc files and enables unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies for Postgres and health checks
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source and migrations
COPY src/ ./src/
COPY migrations/ ./migrations/

# Create the internal volume mount point
RUN mkdir /data_monitor

# Set execution context
WORKDIR /app/src

# Start the service with the internal path
CMD ["python", "service.py", "/data_monitor"]