# API Service

FastAPI service exposing patient and evaluation/worklist data for the web app.

## Run (Docker Compose)

From repo root:

```bash
docker compose up --build api-service
```

Service runs on `http://localhost:8000`.

## Endpoints

### Patients

- `GET /api/patients/`
  - Query params: `skip`, `limit`, optional `last_name`, `external_id`
- `GET /api/patients/{patient_id}`

### Evaluation / Worklist

- `GET /api/evaluation/`
  - Query params: `skip`, `limit`, optional `program_name`, `specialty_need_name`, `task_type`
- `GET /api/evaluation/{patient_id}`

## Response Shape (evaluation row)

Typical fields returned by evaluation endpoints include:
- `row_id`
- `patient_id`
- `program_name`
- `tier_name`
- `previous_specialty_encounter`
- `specialty_need_name`
- `needs`
- `encounter_date`
- `last_evaluated_at`
- `days_since_last_evaluation`
- `cadence_days`
- `task_type`

## Docs

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
