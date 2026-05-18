# Jomingos Backend - Deployment Guide

## Overview
This guide explains how to deploy the Jomingos backend without including the database file in version control.

## Important: Database NOT in GitHub

**This is intentional and correct.** The database file (`db.sqlite3`) is:
- **Excluded from GitHub** via `.gitignore`
- **Created fresh on deployment** using migration scripts
- **Populated with test data** using the seed script

This is industry best practice for security and flexibility.

---

## Deployment Steps

### 1. Clone Repository
```bash
git clone <your-repository-url>
cd JOMINGOS/backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
Create a `.env` file:
```bash
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,localhost
```

### 5. Initialize Database
```bash
# Apply migrations
python manage.py migrate

# Create superuser for admin
python manage.py createsuperuser

# (Optional) Seed test patient data
python manage.py seed_patients
```

### 6. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 7. Run Server
```bash
# Development
python manage.py runserver 0.0.0.0:8000

# Production (using gunicorn)
pip install gunicorn
gunicorn Jomingos.wsgi:application --bind 0.0.0.0:8000
```

---

## Hosting Platforms

### Heroku
```bash
heroku login
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
heroku run python manage.py seed_patients
```

### PythonAnywhere
1. Upload code via Git
2. Create virtual environment
3. Run setup commands above
4. Configure web app to use Django app

### AWS/DigitalOcean/Linode
1. SSH into server
2. Clone repository
3. Follow deployment steps above
4. Use systemd to manage Django service
5. Configure Nginx as reverse proxy

### Azure App Service
1. Deploy via GitHub integration
2. Configure app settings in portal
3. Run startup commands
4. Database will persist in Azure Storage

---

## Database Management

### Seed Patient Data
```bash
python manage.py seed_patients
```

Creates 10 test patients for testing/demo purposes.

### Backup Database
```bash
# Create backup
cp db.sqlite3 db.sqlite3.backup

# Restore from backup
cp db.sqlite3.backup db.sqlite3
```

### Reset Database (Development Only)
```bash
# Delete database
rm db.sqlite3

# Recreate and seed
python manage.py migrate
python manage.py seed_patients
```

---

## Production Considerations

### Security
- Set `DEBUG = False` in production
- Use strong `SECRET_KEY`
- Configure `ALLOWED_HOSTS` properly
- Use HTTPS (Let's Encrypt)
- Keep dependencies updated

### Performance
- Use PostgreSQL instead of SQLite for production
- Configure Redis for caching
- Enable gzip compression
- Use CDN for static files
- Set up database backups

### Monitoring
- Enable error logging (Sentry)
- Monitor performance (New Relic, Datadog)
- Set up health checks
- Configure uptime monitoring

---

## Troubleshooting

### "No such table: accounts_user"
**Solution:** Run migrations
```bash
python manage.py migrate
```

### "Patient records missing"
**Solution:** Run seed script
```bash
python manage.py seed_patients
```

### "Static files not found"
**Solution:** Collect static files
```bash
python manage.py collectstatic
```

### "ALLOWED_HOSTS error"
**Solution:** Configure .env file
```bash
DJANGO_ALLOWED_HOSTS=yourdomain.com,localhost
```

---

## What's in GitHub

✓ Source code
✓ Models and views
✓ Templates and static files
✓ Migrations
✓ Management commands (including seed_patients)
✓ Requirements.txt
✓ Configuration files

## What's NOT in GitHub

✗ Database file (db.sqlite3)
✗ Virtual environment
✗ .env file
✗ __pycache__ directories
✗ Local uploads/media files

This is correct and follows Django best practices.

---

## Quick Deploy Command

For quick deployment on a fresh server:

```bash
git clone <repo> && cd JOMINGOS/backend && \
python -m venv venv && \
source venv/bin/activate && \
pip install -r requirements.txt && \
python manage.py migrate && \
python manage.py createsuperuser && \
python manage.py seed_patients && \
python manage.py collectstatic --noinput && \
python manage.py runserver 0.0.0.0:8000
```

---

## Support

For issues or questions, check:
1. Django documentation: https://docs.djangoproject.com/
2. DRF documentation: https://www.django-rest-framework.org/
3. This repository's README.md
