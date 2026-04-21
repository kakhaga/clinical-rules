# Use an official lightweight Python image
FROM python:3.13-slim

# Set environment variables
# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /code

# Install system dependencies (required for psycopg2-binary and general tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application code
COPY app/ ./app/
COPY main.py .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
# We use 'main:app' because your main.py is in the root
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]