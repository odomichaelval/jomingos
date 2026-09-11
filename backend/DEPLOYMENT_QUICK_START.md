# Quick Start Deployment Checklist

Follow these steps to deploy your Jomingos backend to Render in ~15 minutes.

## 1. Prepare Your Repository (3 minutes)

```bash
# Navigate to your backend directory
cd JOMINGOS/backend

# Make sure you're on the main/master branch
git checkout main

# Stage all new files (Procfile, .gitignore, DEPLOYMENT guides)
git add Procfile .gitignore DEPLOYMENT.md DEPLOYMENT_RENDER.md

# Check what will be committed
git status

# Important: Verify db.sqlite3 is NOT listed
# If it is, run: git rm --cached db.sqlite3

# Commit
git commit -m "Add deployment configuration and guides"

# Push to GitHub
git push origin main
```

## 2. Update requirements.txt (2 minutes)

Open `requirements.txt` and add these two lines at the end:

```
gunicorn>=21.2.0,<22.0
psycopg2-binary>=2.9.0,<3.0
```

Commit:
```bash
git add requirements.txt
git commit -m "Add gunicorn and psycopg2 for production"
git push origin main
```

## 3. Create Render Account (2 minutes)

1. Go to https://render.com
2. Sign up with GitHub (easier)
3. Authorize GitHub access

## 4. Create PostgreSQL Database (3 minutes)

1. In Render dashboard: "New +" → "PostgreSQL"
2. Fill in:
   - Name: `jomingos-postgres`
   - Database: `jomingos_db`
   - User: `jomingos_user`
   - Region: Choose nearest to you
   - Instance Type: **Free**
3. Click "Create Database"
4. **Save the Internal Database URL** (copy the full URL)

## 5. Create Web Service (3 minutes)

1. In Render dashboard: "New +" → "Web Service"
2. Connect GitHub repo (select `JOMINGOS`)
3. Fill in:
   - Name: `jomingos-backend`
   - Environment: `Python 3`
   - Build Command: 
     ```
     pip install -r requirements.txt && python manage.py collectstatic --noinput
     ```
   - Start Command: 
     ```
     gunicorn Jomingos.wsgi:application --bind 0.0.0.0:$PORT
     ```
   - Instance Type: **Free**

4. Click "Create Web Service"
5. **Copy your app URL** (e.g., `https://jomingos-backend-xyz.onrender.com`)

## 6. Add Environment Variables (3 minutes)

In your Web Service dashboard → **Environment**:

Add these variables (fill in YOUR values):

```
DJANGO_SECRET_KEY=change-me-to-something-random-and-long-at-least-50-chars
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=jomingos-backend-xyz.onrender.com,localhost
DJANGO_DB_ENGINE=django.db.backends.postgresql
DJANGO_DB_NAME=jomingos_db
DJANGO_DB_USER=jomingos_user
DJANGO_DB_PASSWORD=PASTE_PASSWORD_FROM_DATABASE_URL
DJANGO_DB_HOST=PASTE_HOST_FROM_DATABASE_URL
DJANGO_DB_PORT=5432
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend-domain.com
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
FRONTEND_URL=http://localhost:3000
```

**How to extract database details from the URL:**

Internal Database URL looks like:
```
postgresql://jomingos_user:PASSWORD@host.render.internal:5432/jomingos_db
```

Extract:
- `DJANGO_DB_HOST`: `host.render.internal`
- `DJANGO_DB_PASSWORD`: `PASSWORD`
- `DJANGO_DB_USER`: `jomingos_user`
- `DJANGO_DB_NAME`: `jomingos_db`

## 7. Generate a Strong Secret Key

Run this in Python:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Copy the output and paste into `DJANGO_SECRET_KEY` environment variable.

## 8. Deploy (2 minutes)

1. When all environment variables are added, Render will auto-trigger a deployment
2. Watch the **Logs** tab for deployment progress
3. When you see "Build successful" and the status is **Live**, you're deployed! ✅

## 9. Initialize Database (2 minutes)

1. Click **Shell** in your Web Service dashboard
2. Run these commands:

```bash
# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Seed test patient data
python manage.py seed_patients
```

When asked for admin details, choose:
- Username: `admin`
- Email: `admin@jomingos.local`
- Password: Something secure (at least 8 chars, mix of letters/numbers/symbols)

## 10. Test Your Deployment (2 minutes)

1. Go to: `https://jomingos-backend-xyz.onrender.com/api/`
   - You should see the REST API interface
2. Go to: `https://jomingos-backend-xyz.onrender.com/admin/`
   - Log in with admin credentials from Step 9
   - Check that patients are visible
3. Go to: `https://jomingos-backend-xyz.onrender.com/api/swagger/`
   - You should see interactive API documentation

## ✅ You're Live!

Your backend is now running on Render. Share this URL with your frontend team:
```
https://jomingos-backend-xyz.onrender.com
```

## Common Issues & Fixes

### "Internal Server Error" or "Application Error"
→ Check logs: Click **Logs** tab in Render dashboard
→ Look for error messages and fix accordingly

### "Connection refused" for database
→ Database might not be ready yet
→ Wait 30 seconds and refresh
→ Run migrations again in Shell

### "Static files not found"
→ Run in Shell: `python manage.py collectstatic --noinput`

### Need to update your app?
→ Just push to GitHub: `git push origin main`
→ Render will auto-deploy in ~2 minutes

---

**Estimated time: 15-20 minutes from start to fully live** ⏱️

Need help? Check:
- DEPLOYMENT_RENDER.md (detailed guide)
- DEPLOYMENT.md (general guide)
- Django docs: https://docs.djangoproject.com/
