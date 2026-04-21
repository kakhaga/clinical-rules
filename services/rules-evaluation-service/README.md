# Rules Evaluation Service

## 🚀 Getting Started
Prerequisites

    Docker and Docker Compose

    A PostgreSQL database (accessible via DATABASE_URL)

Environment Variables

Create a .env file in the root directory:
Code snippet

DATABASE_URL=postgresql://user:password@localhost:5432/dbname
POLL_INTERVAL=60
DELAY_START=10

Running with Docker

The easiest way to run the service along with its dependencies:
Bash

docker-compose up --build

Running Locally

    Create a virtual environment: python -m venv venv && source venv/bin/activate

    Install dependencies: pip install -r requirements.txt

    Run the service: python -m app.main

⚙️ How It Works

    Polling: The service runs in a persistent loop, sleeping for POLL_INTERVAL between cycles.

    Data Fetching: It queries the care.patient_diagnoses view to get the latest clinical data.

    Evaluation: The RulesEngine passes data through registered strategies (e.g., DiabetesManagementStrategy).

    ID Mapping: String-based results are mapped to database IDs using cached lookups from dim_program and dim_risk_tier.

    Bulk Upsert: Results are de-duplicated in Python and then sent to PostgreSQL using an ON CONFLICT DO UPDATE (Upsert) operation for maximum performance.

🛠 Development
Adding a New Strategy

    Create a new file in app/strategies/.

    Implement your logic within a class.

    Register the strategy in app.services.evaluation_service.

Database Migrations

This project uses Alembic for migrations.

    Generate a migration: alembic revision --autogenerate -m "description"

    Apply migrations: alembic upgrade head

🐳 Docker Details

    Entrypoint: The entrypoint.sh script automatically runs alembic upgrade head before starting the service to ensure the schema is up to date.

    Healthchecks: The service is configured to wait for the ingestion-service (if present) before starting.