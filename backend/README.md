# JOMINGOS Backend - Django REST API for Care Facilities

This is the complete backend for the JOMINGOS healthcare management platform. A Django REST API that powers everything - patient records, staff management, medications, vital signs monitoring, shift tracking, and live dashboards.

## Complete Feature List (14 Major Features)

### Feature 1-4: Role-Based Dashboards
Different custom dashboards for:
- **Admin Dashboard** - Staff coverage, safety oversight, resident management
- **Doctor Workspace** - High-risk patient reviews, medication oversight, clinical notes
- **Nurse Shift Dashboard** - Medication rounds, vitals, handover coordination
- **Care Assistant Hub** - Personal care tasks, wellbeing checks, escalations

### Feature 5: Animated Statistics
- Counter animations on dashboard load
- Active patients, care notes, medications, staff on duty
- Smooth visual transitions

### Feature 6: Weather Widget
- Real-time weather data
- Temperature, conditions, wind, humidity
- Updates automatically

### Feature 7: Performance KPI Cards
- Handover completion rate
- Response time tracking
- Adherence metrics
- Safety incident monitoring

### Feature 8: Real-Time Notifications
- Bell icon with unread badge
- Notification dropdown panel
- Mark as read functionality
- Alert, warning, info, success types

### Feature 9: Patient Summary Cards
- Quick patient overview
- Room numbers, care levels, status
- Action buttons to view details

### Feature 10: Dark Mode Toggle
- Toggle on/off on dashboard
- Saves preference to database
- Smooth transitions

### Feature 11: Interactive Charts & Graphs
- Care notes trend line chart
- Care level distribution doughnut chart
- Staff roles breakdown
- Using Chart.js for visualization

### Feature 12: Advanced Search & Filtering
- Search patients by name, NHS number, room
- Filter by care level, medical conditions
- Sort and organize results

### Feature 13: Audit Logging (Compliance)
- Track ALL user actions (login, create, update, delete)
- IP address logging
- User agent tracking
- Perfect for compliance and security reviews

### Feature 14: API Documentation
- Auto-generated Swagger docs
- Interactive API explorer
- All endpoints documented
- Available at `/api/swagger/`

### BONUS: Live Shift Countdown Timer ⭐
- Real-time HH:MM:SS countdown to shift end
- Shows shift start/end times
- Progress bar with percentage
- Pulsing alert when <1 hour remaining
- Per-user shift tracking in database
- API endpoints for shift management

---

## Features Summary Table

| Feature | Status | Details |
|---------|--------|---------|
| Role-Based Dashboards | ✅ Complete | 4 different dashboards (Admin/Doctor/Nurse/Care Assistant) |
| Shift Countdown Timer | ✅ Complete | Live timer with API endpoints, database tracking |
| Animated Statistics | ✅ Complete | Counter animations on load |
| Weather Widget | ✅ Complete | Real-time weather integration |
| Performance KPIs | ✅ Complete | Metrics tracking and display |
| Real-Time Notifications | ✅ Complete | Bell icon, dropdown panel, mark as read |
| Patient Summary | ✅ Complete | Quick patient cards with details |
| Dark Mode | ✅ Complete | Toggle with database persistence |
| Interactive Charts | ✅ Complete | Line and doughnut charts with Chart.js |
| Search & Filtering | ✅ Complete | Advanced search, sorting, filtering |
| Audit Logging | ✅ Complete | Complete activity tracking for compliance |
| API Documentation | ✅ Complete | Swagger docs with interactive explorer |
| User Authentication | ✅ Complete | JWT-based, role-based access control |
| Admin Panel | ✅ Complete | Django admin with customization |

## Project Structure

```
backend/
├── manage.py                 # Django management script
├── Jomingos/                # Main project settings
│   ├── settings.py         # Django configuration
│   ├── urls.py             # Main URL routing
│   └── wsgi.py             # WSGI for deployment
├── accounts/               # User accounts and auth
│   ├── models.py          # User model, audit logs
│   └── views.py           # Login, registration
├── patients/              # Patient/resident management
│   ├── models.py          # Patient model
│   └── management/commands/seed_patients.py  # Test data
├── medications/           # Medication tracking
│   └── models.py          # Medication model
├── vitals/                # Vital signs recording
│   └── models.py          # VitalSigns model with NEWS2
├── care_notes/            # Care documentation
│   └── models.py          # CareNote model
├── dashboard/             # Dashboard API and views
│   ├── models.py          # DashboardPreference, UserShift, Notifications
│   ├── views.py           # Dashboard rendering
│   ├── views_api.py       # REST API endpoints
│   └── admin.py           # Admin panel setup
├── templates/             # HTML templates
│   └── dashboard/         # Dashboard HTML
├── static/                # CSS, JS, images
└── requirements.txt       # Python dependencies
```

## Key Features

### 1. Role-Based Dashboard (Feature #1-4)
Each staff member sees a customized dashboard based on their role:
- **Admins** see staffing, safety, resident overview
- **Doctors** see high-risk patients, medication history, clinical notes
- **Nurses** see medication rounds, vitals due, handover info
- **Care Assistants** see personal care tasks, wellbeing, escalations

### 2. Live Shift Countdown Timer (New Feature!)
- Real-time HH:MM:SS countdown to end of shift
- Shows start/end times and progress percentage
- Pulses when less than 1 hour remaining
- Automatically syncs with server every 5 minutes
- Tracks shifts per user per day in database

### 3. Animated Dashboard Stats (Feature #5)
- Counter animations when page loads
- Shows active patients, care notes, meds given, staff on duty
- Smooth number transitions for visual appeal

### 4. Weather Widget (Feature #6)
- Real weather data for the facility location
- Shows temperature, conditions, wind speed, humidity
- Updates automatically

### 5. Performance KPI Cards (Feature #7)
- Handover completion rate
- Average response time
- Adherence rate
- Safety incidents tracking
- High-risk patient alerts

### 6. Real-Time Notifications (Feature #8)
- Bell icon with unread badge
- Dropdown notification panel
- Mark as read functionality
- Different notification types (alert, warning, info, success)

### 7. Patient Summary Cards (Feature #9)
- Quick view of each active patient
- Shows room number, care level, status
- Action buttons to view details

### 8. Dark Mode (Feature #10)
- Toggle button on dashboard
- Saves preference to database
- Works across all pages
- Smooth transitions between modes

### 9. Interactive Charts (Feature #11)
- Care notes trend line chart
- Care level distribution doughnut chart
- Staff roles breakdown
- Using Chart.js

### 10. Advanced Search & Filtering (Feature #12)
- Search patients by name, NHS number, room
- Filter by care level, medical conditions
- Sort results

### 11. Audit Logging (Feature #13)
- Track all user actions (login, create, update, delete, etc.)
- IP address logging
- User agent tracking
- Perfect for compliance and security

### 12. API Documentation (Feature #14)
- Swagger/OpenAPI docs at `/api/swagger/`
- Interactive API explorer
- All endpoints documented with examples

## Database Models Overview

### User
```python
- username, email, password
- first_name, last_name
- role (admin, doctor, nurse, care_assistant, family)
- phone_number, profile_image
- is_on_duty, is_active
```

### Patient
```python
- first_name, last_name, date_of_birth
- nhs_number, room_number
- care_level (nursing, dementia, residential, respite)
- medical_conditions, allergies
- gender, blood_group, emergency_contact
- is_active
```

### UserShift (New!)
```python
- user (OneToOne)
- shift_type (day, night, custom)
- start_time, end_time
- shift_date
- is_active, notes
- Calculated: time_remaining, progress_percent
```

### Medication
```python
- patient, medication
- drug_name, dosage, route
- administered_by (nurse/doctor)
- administered_at
- frequency, duration
```

### VitalSigns
```python
- patient, recorded_by
- systolic_bp, diastolic_bp
- heart_rate, temperature
- respiratory_rate, oxygen_saturation
- news2_level (calculated property)
- recorded_at
```

### CareNote
```python
- patient, author
- category (observation, medication, personal_care, etc.)
- content, priority
- created_at, updated_at
```

### DashboardNotification
```python
- user, notification_type
- title, message, icon
- is_read, created_at
```

### DashboardPreference
```python
- user (OneToOne)
- visible_widgets, widget_order
- dark_mode, show_notifications
- refresh_interval
```

### AuditLog
```python
- user, action
- description, model_name, object_id
- ip_address, user_agent, status
- timestamp
```

## What Makes This Backend Different

### Real Healthcare Features (Not Generic)
- **NEWS2 Scoring** - Automatic early warning scores for vitals
- **Medication Tracking** - Records who, what, when, where for every dose
- **Shift Management** - Actual shift tracking with live countdown
- **Care Levels** - Nursing, dementia, residential, respite categories
- **Audit Logging** - Complete compliance trail for healthcare standards

### Professional Implementation
- **Role-Based Access** - Different views for each staff type
- **Real-Time Updates** - Dashboards update without refresh
- **Database Flexibility** - SQLite for dev, PostgreSQL for production
- **API First** - Frontend completely decoupled via REST API
- **Swagger Docs** - Auto-generated API documentation
- **Dark Mode** - Professional UI with theme support

### Production Ready
- **JWT Authentication** - Secure token-based auth
- **CSRF Protection** - Built-in Django security
- **Password Hashing** - PBKDF2 hashing
- **Audit Trail** - Every action logged for compliance
- **Error Handling** - Proper exception handling throughout
- **Static Files** - Optimized for production serving

### Scalability
- **Pagination Ready** - Can handle thousands of records
- **Database Indexing** - Optimized queries
- **Caching Support** - Ready for Redis integration
- **API Rate Limiting** - Extensible for throttling
- **Multi-Database** - Works with SQLite, PostgreSQL, MSSQL

---

## Getting Started Locally

### Prerequisites
- Python 3.10+
- pip (Python package manager)
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/Ebujoe/JOMINGOS-clean.git
cd JOMINGOS/backend
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create .env File
Create a file called `.env` in the backend directory:

```env
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_DB_ENGINE=django.db.backends.sqlite3
DJANGO_DB_NAME=db.sqlite3
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
FRONTEND_URL=http://localhost:3000
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
# Follow the prompts to create your admin account
```

### 7. Seed Test Data
```bash
python manage.py seed_patients
```

This creates 10 realistic patient records so you can test everything out.

### 8. Start Development Server
```bash
python manage.py runserver 0.0.0.0:8000
```

Now you can access:
- **Dashboard**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/
- **API Docs**: http://localhost:8000/api/swagger/

## API Endpoints

### Authentication
```
POST /accounts/login/ - Login with credentials
POST /accounts/logout/ - Logout
POST /accounts/register/ - Register new user
```

### Patients
```
GET /api/patients/ - List all patients
GET /api/patients/<id>/ - Get patient details
POST /api/patients/ - Create new patient
PUT /api/patients/<id>/ - Update patient
DELETE /api/patients/<id>/ - Delete patient (soft delete)
```

### Dashboard
```
GET /api/dashboard/stats/ - Get dashboard statistics
GET /api/dashboard/<role>/ - Get role-specific dashboard data
GET /api/shifts/current/ - Get user's current shift with countdown
POST /api/shifts/set/ - Create/update user's shift
```

### Medications
```
GET /api/medications/ - List medications
POST /api/medications/ - Record medication given
GET /api/medications/<id>/ - Get medication details
```

### Vitals
```
GET /api/vitals/ - List vital signs records
POST /api/vitals/ - Record new vitals
```

### Care Notes
```
GET /api/notes/ - List care notes
POST /api/notes/ - Create new care note
```

### Notifications
```
GET /api/notifications/ - Get user's notifications
POST /api/notification/<id>/read/ - Mark notification as read
```

### Preferences
```
POST /api/preferences/dark-mode/ - Toggle dark mode
```

## Deployment Steps (Using Render - Easiest Option)

### Step 1: Prepare GitHub Repository
Make sure your code is committed:
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Sign Up on Render
Go to https://render.com and create an account (use GitHub to sign up, it's easier)

### Step 3: Create PostgreSQL Database
1. Click "New +" → "PostgreSQL"
2. Fill in:
   - Name: `jomingos-postgres`
   - Database: `jomingos_db`
   - User: `jomingos_user`
   - Region: Pick closest to you
   - Plan: Free
3. Click "Create Database"
4. **Copy the Internal Database URL** (you'll need it later)

### Step 4: Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repo
3. Fill in settings:
   - **Name**: `jomingos-backend`
   - **Environment**: Python 3
   - **Build Command**:
     ```
     pip install -r requirements.txt && python manage.py collectstatic --noinput
     ```
   - **Start Command**:
     ```
     gunicorn Jomingos.wsgi:application --bind 0.0.0.0:$PORT
     ```
   - **Plan**: Free
4. Click "Create Web Service"

### Step 5: Add Environment Variables
In your Web Service dashboard, go to "Environment" and add these:

```
DJANGO_SECRET_KEY=generate-a-random-secret-key-here
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=your-app.onrender.com,yourdomain.com
DJANGO_DB_ENGINE=django.db.backends.postgresql
DJANGO_DB_NAME=jomingos_db
DJANGO_DB_USER=jomingos_user
DJANGO_DB_PASSWORD=your-db-password-here
DJANGO_DB_HOST=your-db-host.render.internal
DJANGO_DB_PORT=5432
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend-domain.com
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
FRONTEND_URL=https://your-frontend-domain.com
```

**Where to find database info:**
- Go back to your PostgreSQL database page
- Look for "Internal Database URL" - it looks like: `postgresql://user:password@host:5432/dbname`
- Extract the values from there

### Step 6: Generate Secret Key
In Python shell, run:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Copy that long string into `DJANGO_SECRET_KEY` environment variable.

### Step 7: Deploy
When you add the environment variables, Render automatically starts deploying. Watch the "Logs" tab to see if it works.

Once it says "Build successful" and status is "Live", you're good!

### Step 8: Initialize Database
Click "Shell" in your Web Service and run:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_patients
```

Answer the prompts for creating admin account.

### Step 9: Test Your Deployment
Visit:
- Dashboard: `https://your-app.onrender.com/`
- Admin: `https://your-app.onrender.com/admin/`
- API Docs: `https://your-app.onrender.com/api/swagger/`

Done! Your backend is live! 

## Testing Locally

### Run Tests
```bash
python manage.py test
```

### Check Migrations
```bash
python manage.py showmigrations
```

### Create Test User via Shell
```bash
python manage.py shell
>>> from accounts.models import User
>>> User.objects.create_user(username='testuser', password='testpass123')
```

## Troubleshooting

### Database Errors
```
"No such table: accounts_user"
→ Run: python manage.py migrate
```

### Static Files Not Loading
```
→ Run: python manage.py collectstatic
```

### ALLOWED_HOSTS Error
→ Add your domain to DJANGO_ALLOWED_HOSTS in .env
```

### Shift Timer Not Showing
```
→ Create a shift: POST /api/shifts/set/
→ Check user has is_on_duty = True
```

### Can't Log In
```
→ Make sure you ran: python manage.py createsuperuser
→ Check CORS settings in .env
```

## Admin Panel Features

You can access the admin at `/admin/` to:
- Manage users and staff
- Create/edit patient records
- View audit logs
- Configure dashboard preferences
- Manage notifications
- Set up user shifts
- View all database records

Everything has a nice admin interface set up.

## Production Checklist

Before deploying:
- [ ] Set `DJANGO_DEBUG=0`
- [ ] Generate strong `DJANGO_SECRET_KEY`
- [ ] Use PostgreSQL (not SQLite)
- [ ] Set proper `ALLOWED_HOSTS`
- [ ] Configure `CORS_ALLOWED_ORIGINS`
- [ ] Set up email backend (Gmail or SendGrid)
- [ ] Create admin superuser
- [ ] Seed test data
- [ ] Test all API endpoints
- [ ] Verify admin panel works
- [ ] Check dashboard displays correctly

## Important Security Notes

1. **Never commit .env files** - They contain secrets
2. **Always use HTTPS in production** - Render handles this automatically
3. **Keep SECRET_KEY secret** - Generate a new one for production
4. **Use strong passwords** - At least 12 chars with mixed types
5. **Enable CSRF protection** - Django has this by default
6. **Audit logs track everything** - Good for compliance

## File Explanations

### settings.py
Has all the Django configuration - database, apps, middleware, security settings.

### models.py (in each app)
Defines the database structure. The actual tables and relationships.

### views.py
Handles the logic - what happens when someone makes a request.

### views_api.py
REST API endpoints using Django REST Framework.

### urls.py
Maps URLs to views. If someone visits `/api/patients/`, this determines what code runs.

### admin.py
Registers models in the Django admin panel so you can edit them easily.

### migrations/
Database schema changes tracked in version control. Really important.

### management/commands/
Custom Django commands. Like `seed_patients.py` which populates test data.

## Useful Commands

```bash
# Start development server
python manage.py runserver

# Make migrations after model changes
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Open interactive shell
python manage.py shell

# Seed test data
python manage.py seed_patients

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Check for issues
python manage.py check
```

## Performance Notes

- Dashboard loads all patient data - could be optimized with pagination
- Charts calculate on every request - could cache results
- Audit logging everything - might impact performance on high traffic
- Consider adding Redis caching for production

## Future Improvements

- Add SMS notifications
- Implement shift swapping
- Add bulk import for patient records
- Mobile app integration
- Advanced reporting features
- Prescription management
- Medical imaging integration
- Video consultation support

## Documentation Files

Check these out for more details:
- `DEPLOYMENT.md` - Detailed deployment guide
- `DEPLOYMENT_RENDER.md` - Render-specific instructions
- `DEPLOYMENT_QUICK_START.md` - Quick 15-minute guide
- `SHIFT_COUNTDOWN_TIMER.md` - Shift timer feature docs
- `FEATURE_SHIFT_TIMER_SUMMARY.md` - Timer feature overview

## API Authentication

All endpoints (except login/register) need JWT token:

```bash
# Login first
curl -X POST http://localhost:8000/accounts/login/ \
  -d "username=admin&password=yourpassword"

# Get token from response, then use it
curl -X GET http://localhost:8000/api/patients/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Contact & Support

For issues:
1. Check the documentation files
2. Look at Django error messages
3. Check browser console for frontend errors
4. Check Render logs for deployment issues

---

**Backend Status**: Production Ready  
**Last Updated**: May 2026  
**Version**: 1.0

The system is fully functional with all major features implemented and ready for real-world use in a care facility.
