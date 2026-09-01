# Personal Health Companion Backend

FastAPI backend for the personal health companion. It stores authenticated patient-owned records in SQLite and uses a **temporary rule-based risk engine** for integration only; it is not an ML model or medical diagnostic system.

## Installation

From `backend/` on Windows:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set a strong `SECRET_KEY`. `DATABASE_URL` defaults to `sqlite:///./data/health.db`; the actual file is created at `backend/data/health.db` and is ignored by Git.

## Run

```powershell
uvicorn app.main:app --reload
```

API root: `http://localhost:8000`  
Swagger: `http://localhost:8000/docs`

The development CORS origin is configured through `FRONTEND_ORIGIN` (default `http://localhost:5173`).

## Authentication

Register at `POST /api/auth/register`, then exchange email/password at `POST /api/auth/login`. Send the returned token on protected calls as `Authorization: Bearer <token>`. Passwords are Argon2 hashes, never plaintext.

## Endpoints

- `GET /`, `GET /health`
- `POST /api/auth/register`, `POST /api/auth/login`
- `GET|PUT /api/patients/me`
- `POST /api/health/readings`, `GET /api/health/latest`, `GET /api/health/history`
- `POST /api/environment/readings`, `GET /api/environment/latest`, `GET /api/environment/history`
- `GET /api/risk/latest`, `GET /api/risk/history`
- `GET /api/dashboard`
- `GET /api/alerts`, `POST /api/alerts/{alert_id}/resolve`
- `GET /api/recommendations`, `POST /api/emergency/sos`
- `POST /api/device/readings`
- `GET /api/reports/csv`, `GET /api/reports/pdf`

## Tests

```powershell
pytest
```

Tests use a temporary SQLite database and do not alter the development database.

## Frontend integration

No frontend files are changed. The future React API service should call `http://localhost:8000/api/...`, pass the JWT bearer token, and replace only existing dummy-data consumption after the backend contract is accepted.
