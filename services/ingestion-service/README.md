## 🚀 Getting Started

### 1. Prerequisites
* Docker and Docker Compose
* PostgreSQL (Local or Dockerized)

### 2. Configuration
Create a `.env` file in the root directory (see template `.env.template`):

```env
DB_USER=database_user
DB_PASSWORD=database_password
DB_HOST=host.docker.internal    # Use docker-network if postgres is in compose
DB_PORT=5432
DB_NAME=database_name
DB_LOGS=False                   # Whether to output SQL commands executed in stdout
POLL_INTERVAL=60                # Check folder every 60 seconds
```

***IMPORTANT: In PostgreSQL, make sure to create database and grant the connecting user the create permissions:***
```
CREATE DATABASE <DB_NAME>;
GRANT CREATE ON DATABASE clinical_rules TO <DB_USER>;
```

### 3. Build and Run
```bash
docker-compose up --build -d
```

## 🛠 Features
* **High Performance:** Uses PostgreSQL `COPY` command via `psycopg2` for rapid data loading.
* **Data Integrity:** Implements `DISTINCT ON` and `ON CONFLICT` logic to prevent duplicate patient records and cardinality violations.
* **Containerized:** Fully portable environment using the latest stable Python 3.13.
* **Automated Migrations:** Automatically applies SQL updates from the `migrations/` folder on startup.

## 📝 Usage
Drop the following files into the `./data` folder:
* `patients.csv`
* `diagnoses.csv`
* `labs.csv`
* `encounters.csv`

The service will detect the files, process them, and log the status to the Docker console.

## 🔍 Monitoring Logs
```bash
docker logs -f clinical_ingestion_app
```