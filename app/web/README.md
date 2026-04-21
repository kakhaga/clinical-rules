# Clinical Rules Web App

Frontend for the Clinical Rules Engine. Built with React + TypeScript + Vite.

## Features

- Shared app layout with sidebar navigation.
- Dashboard summary from `/api/evaluation/` and `/api/patients/`.
- Patients page with:
  - paginated list mode (`skip`/`limit`)
  - patient-id lookup mode (`/api/patients/{patient_id}`)
- Tasks page with:
  - evaluation worklist from `/api/evaluation/`
  - Clinical Team vs Scheduler view toggle
  - dropdown filters (`program_name`, `specialty_need_name`, `task_type`)
  - patient-id lookup (`/api/evaluation/{patient_id}`)

## Run Locally

```bash
npm install
npm run dev
```

App runs at `http://localhost:5173`.

## Build

```bash
npm run build
```

## API Expectations

Vite proxies `/api` to `http://localhost:8000`.

Required routes:
- `GET /api/patients/`
- `GET /api/patients/{patient_id}`
- `GET /api/evaluation/`
- `GET /api/evaluation/{patient_id}`
