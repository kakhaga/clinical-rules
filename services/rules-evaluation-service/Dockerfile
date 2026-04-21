FROM python:3.13-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Set the project root in the python path
ENV PYTHONPATH=/code

# Set working directory
WORKDIR /code

# Install system dependencies (needed for psycopg2 or other C-based extensions)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
# We copy everything so alembic.ini and migrations are available

COPY alembic.ini .
COPY requirements.txt .

# Copy the actual application and migration logic
COPY app/ ./app/
COPY migrations/ ./migrations/

# Copy shell script
COPY entrypoint.sh .

# Make the entrypoint script executable
RUN chmod +x /code/entrypoint.sh

# Use the script to start the container
ENTRYPOINT ["/code/entrypoint.sh"]