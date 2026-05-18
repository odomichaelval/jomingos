# Deploying Jomingos Backend to Render

Render is a modern alternative to Heroku with a free tier. Follow these steps to deploy your Django app.

## Prerequisites

- GitHub account with your Jomingos repository pushed
- Render.com account (free)

## Step 1: Prepare Your Repository

Make sure these files are in your GitHub repository:

```
JOMINGOS/backend/
├── manage.py
├── Jomingos/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── requirements.txt
├── .gitignore  (contains: db.sqlite3, .env, venv/, __pycache__/)
└── Procfile  (create this next)
```

## Step 2: Create Procfile

Create a file named `Procfile` in your backend directory (no extension):

```
web: gunicorn Jomingos.wsgi:application --bind 0.0.0.0:$PORT
release: python manage.py migrate && python manage.py createsuperuser --noinput || true
```

Commit this to GitHub:
```bash
git add Procfile
git commit -m "Add Procfile for Render deployment"
git push origin main
```

## Step 3: Update requirements.txt

Add gunicorn to your requirements.txt:

```
Django>=4.2,<5.0
Pillow>=10.0.0
djangorestframework>=3.15,<4.0
djangorestframework-simplejwt>=5.3,<6.0
django-cors-headers>=4.3,<5.0
drf-yasg>=1.21.7,<2.0
mssql-django>=1.4,<2.0
pyodbc>=5.0,<6.0
whitenoise>=6.6,<7.0
python-dotenv>=1.0,<2.0
gunicorn>=21.2.0,<22.0
psycopg2-binary>=2.9.0,<3.0
```

Commit:
```bash
git add requirements.txt
git commit -m "Add gunicorn and psycopg2 for production"
git push origin main
```

## Step 4: Create PostgreSQL Database (Optional but Recommended)

You have two options:

**Option A: Use Render's built-in PostgreSQL (Recommended for production)**
- We'll set this up in the Web Service creation

**Option B: Use SQLite (Simpler, but less scalable)**
- Keep DJANGO_DB_ENGINE=django.db.backends.sqlite3

We'll use Option A below.

## Step 5: Create Web Service on Render

1. Go to https://render.com and sign in
2. Click "New +" → "Web Service"
3. Connect your GitHub account and select your Jomingos repository
4. Configure:
   - **Name**: `jomingos-backend` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn Jomingos.wsgi:application --bind 0.0.0.0:$PORT`
   - **Instance Type**: Free (for now)

5. Click "Create Web Service"

## Step 6: Add Environment Variables

In your Web Service dashboard:

1. Go to **Environment** section
2. Add these variables:

```
DJANGO_SECRET_KEY=your-very-secure-random-string-here (use a strong random key)
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=your-render-app.onrender.com,yourdomain.com,localhost
DJANGO_DB_ENGINE=django.db.backends.postgresql
DJANGO_DB_NAME=jomingos_db
DJANGO_DB_USER=jomingos_user
DJANGO_DB_PASSWORD=(we'll set this from database URL)
DJANGO_DB_HOST=(we'll set this from database URL)
DJANGO_DB_PORT=5432
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend-domain.com
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
FRONTEND_URL=https://your-frontend-domain.com
```

## Step 7: Create PostgreSQL Database on Render

1. In Render dashboard, click "New +" → "PostgreSQL"
2. Configure:
   - **Name**: `jomingos-postgres`
   - **Database**: `jomingos_db`
   - **User**: `jomingos_user`
   - **Region**: Same as your Web Service
   - **Instance Type**: Free

3. Click "Create Database"

4. Once created, you'll see an **Internal Database URL**. Copy it.

5. Go back to your Web Service → Environment
6. Update these variables using values from the database URL:
   - `DJANGO_DB_HOST`: Extract from database URL (hostname part)
   - `DJANGO_DB_PASSWORD`: Extract from database URL (password part)

## Step 8: Deploy

1. Render will auto-deploy when you push to GitHub
2. Check the **Logs** tab in Render dashboard for deployment progress
3. Once the build succeeds (green status), your app is live!

## Step 9: Create Superuser

Option A: Through Render's shell
1. In your Web Service dashboard, click "Shell"
2. Run: `python manage.py createsuperuser`

Option B: Use Render Environment Variable
Add to your environment:
```
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=your-secure-password
DJANGO_SUPERUSER_EMAIL=admin@jomingos.local
```

Then in Procfile, add to release command:
```
release: python manage.py migrate && python manage.py createsuperuser --noinput 2>/dev/null || true && python manage.py seed_patients
```

## Step 10: Seed Patient Data

Option A: Through Render's shell
1. Click "Shell" in your Web Service
2. Run: `python manage.py seed_patients`

Option B: Add to Procfile release command (see Step 9)

## Step 11: Configure Your Frontend

Update your Next.js frontend to point to your Render backend:

```javascript
const API_BASE_URL = 'https://your-render-app.onrender.com/api'
```

## Troubleshooting

### Logs show database errors
- Check that DATABASE_URL environment variable is correctly set
- Verify PostgreSQL database is in the same region as Web Service

### Static files not loading
- Ensure `python manage.py collectstatic --noinput` runs in build command
- Check that STATIC_ROOT and STATIC_URL are correct in settings.py

### App keeps crashing
- Click "Shell" and run: `python manage.py migrate --verbosity 2`
- Check logs for specific error messages

### Slow first deployment
- First deployment takes longer (3-5 mins). Subsequent deployments are faster.

## Production Checklist

- [ ] DJANGO_DEBUG=0
- [ ] DJANGO_SECRET_KEY is strong and random
- [ ] DJANGO_ALLOWED_HOSTS includes your domain
- [ ] CORS_ALLOWED_ORIGINS configured for frontend domain
- [ ] PostgreSQL database created and connected
- [ ] Superuser created
- [ ] Test patient data seeded
- [ ] Frontend points to correct API URL
- [ ] HTTPS enabled (Render handles this automatically)
- [ ] Email backend configured (Gmail or SendGrid recommended)

## Next Steps

After deployment is successful:
1. Test your API at `https://your-render-app.onrender.com/api/`
2. Access admin at `https://your-render-app.onrender.com/admin/`
3. Deploy your Next.js frontend
4. Test end-to-end functionality

---

For more details, see DEPLOYMENT.md in the backend directory.
