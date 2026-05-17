# JOMINGOS Backend

A Django-based healthcare home documentation platform backend with user authentication, profile management, and password change functionality.

## Features

- User authentication (Login/Logout)
- User profile management with file upload
- Self-service password change with complexity requirements
- Role-based access control (Admin, Doctor, Nurse, Care Assistant)
- Staff management system
- WCAG 2.1 AA compliant interface

## Tech Stack

- Django 4.x
- Django REST Framework
- SQLite (development)
- Bootstrap 5
- AdminLTE 4

## Quick Start

### Requirements
- Python 3.8+
- pip
- Virtual environment

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ebujoe/JOMINGOS-clean.git
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run development server:
```bash
python manage.py runserver
```

Server runs at `http://127.0.0.1:8000`

## Project Structure

```
backend/
├── accounts/           # User authentication and profiles
├── templates/          # HTML templates
├── static/            # CSS, JS, images
├── manage.py
└── requirements.txt
```

## Frontend

The frontend is maintained separately and will be integrated via API endpoints.

## License

© 2026 JOMINGOS - Healthcare Home Documentation Platform

