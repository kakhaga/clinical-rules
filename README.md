# Clinical Rules Engine

> Copyright (c) 2026 Nikhil Marwah. All rights reserved.
> This repository is shared solely for evaluation in connection with a hiring process.
> No license is granted to use, copy, modify, merge, publish, distribute, sublicense, sell, deploy, or create derivative works from this software or documentation, in whole or in part, without prior written permission.

Clinical Rules Engine ingests patient data, evaluates clinical need/risk, and exposes API + UI worklists for care operations.

## Repository Layout

- `services/ingestion-service`: loads CSV source data into normalized Postgres schemas.
- `services/rules-evaluation-service`: computes care program evaluations and materializes evaluation views.
- `services/api-service`: FastAPI API for patients and evaluation/task worklists.
- `app/web`: React + TypeScript web app consuming API endpoints through Vite proxy.
- `docs/ARCHITECTURE.md`: high-level architecture and data flow.

## Quick Start

1. Create root `.env` with required DB/API settings used by docker compose.
2. Start services:

```bash
docker compose up --build
```

3. Open apps:
- API docs: `http://localhost:8000/docs`
- Web app: `http://localhost:8080`

## Current API Surface (used by web)

- `GET /api/patients/`
- `GET /api/patients/{patient_id}`
- `GET /api/evaluation/`
- `GET /api/evaluation/{patient_id}`

`/api/evaluation/` supports query params: `skip`, `limit`, `program_name`, `specialty_need_name`, `task_type`.

## Frontend Worklist Modes

Tasks page supports two frontend-only worklist modes:
- `Clinical Team`: all backend rows.
- `Scheduler`: only rows with `task_type === "Scheduling Task"`.

No authentication/authorization is implemented for these modes in this take-home branch.
