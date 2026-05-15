# Jomingos — Healthcare Home Documentation Platform

A Django application for care-home documentation (patients, care notes, medications, vital signs, tasks).

## Quick Start (Local)

```bash
# 1) Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Run migrations
python manage.py makemigrations accounts patients care_notes medications vitals
python manage.py migrate

# 4) Seed demo data (optional)
python manage.py seed_data

# 5) Start the server
python manage.py runserver
```

Open `http://127.0.0.1:8000/`

## Demo Login Credentials

| Role           | Username      | Password |
|----------------|---------------|----------|
| Administrator  | admin         | admin123 |
| Nurse          | nurse.adams   | nurse123 |
| Doctor         | dr.wilson     | doc123   |
| Care Assistant | care.jones    | care123  |

## REST API (for Next.js)

API base path:
- `/api/`

Docs:
- `GET /api/docs/swagger/`
- `GET /api/docs/redoc/`

Auth endpoints:
- `POST /api/accounts/register/`
- `POST /api/accounts/login/`
- `GET /api/accounts/me/`
- `POST /api/accounts/change-password/`

## SQL Server (Azure SQL)

To use SQL Server as the database backend:

1. Copy `backend/.env.example` to `backend/.env`
2. Fill in your Azure SQL connection settings
3. Run migrations:
   - `python manage.py migrate`

## Project Structure

```
backend/
  manage.py
  requirements.txt
  Jomingos/        # Django project settings + URLs
  accounts/        # Custom user + auth
  patients/        # Patient management
  care_notes/      # Care note documentation
  medications/     # Medication administration records
  vitals/          # Vital signs tracking
  tasks/           # Care tasks/checklists
  family/          # Family portal
  dashboard/       # Dashboard + seed command
  templates/       # Django templates (AdminLTE)
  api/             # REST API routing (/api/*)
```

