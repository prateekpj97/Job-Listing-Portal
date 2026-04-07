# Job Listing Portal

A full-featured job listing platform built with Django 4.2. Employers can post and manage jobs; job seekers can browse, filter, and apply.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.2.7 |
| API | Django REST Framework 3.14 |
| Database | PostgreSQL |
| Cache | Redis + django-redis |
| Task Queue | Celery 5.3 + Redis |
| Frontend | Bootstrap 5, jQuery |
| Testing | Pytest + pytest-django |
| Deployment | Docker & Docker Compose |

---

## Features

- **Post Jobs** — Employers create, edit, and delete job listings
- **Apply for Jobs** — Job seekers submit applications with cover letter and resume upload
- **Filtering** — Filter by title, location, job type, category, and salary range
- **Role-based Access** — `employer` and `job_seeker` roles with enforced permissions
- **REST API** — Full CRUD API for jobs and applications with filtering, search, and ordering
- **Async Notifications** — Celery tasks send email on new application and status changes
- **Redis Cache** — Job list responses cached per query string

---

## Project Structure

```
├── apps/
│   ├── accounts/        # Custom User model (employer / job_seeker)
│   ├── jobs/            # Job & Category models, views, API, filters, Celery tasks
│   └── applications/    # Application model, views, API
├── config/              # Django settings, URLs, Celery config
├── templates/           # Bootstrap 5 HTML templates
├── tests/               # Pytest test suite
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Local PostgreSQL running on port 5432

### 1. Clone & configure

```bash
git clone <repo-url>
cd Job-Listing-Portal
cp .env.example .env   # fill in your values
```

### 2. Environment variables (`.env`)

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=jobportal
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=127.0.0.1
DB_PORT=5432

REDIS_URL=redis://127.0.0.1:6379/0
CELERY_BROKER_URL=redis://127.0.0.1:6379/1
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/2

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@jobportal.com
```

### 3. Create the database

```bash
psql -U postgres -h 127.0.0.1 -c "CREATE DATABASE jobportal;"
```

### 4. Run with Docker Compose

```bash
docker compose up --build
docker compose exec web python manage.py makemigrations accounts jobs applications
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

App runs at **http://localhost:8001**

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/jobs/` | List & filter jobs |
| POST | `/api/jobs/` | Create job (employer) |
| GET | `/api/jobs/<id>/` | Job detail |
| PUT/PATCH | `/api/jobs/<id>/` | Update job (owner) |
| DELETE | `/api/jobs/<id>/` | Delete job (owner) |
| GET | `/api/jobs/my_jobs/` | Employer's own jobs |
| GET | `/api/categories/` | List categories |
| GET | `/api/applications/` | List applications (role-filtered) |
| POST | `/api/applications/` | Submit application |
| PATCH | `/api/applications/<id>/` | Update status (employer) |

### Filter params for `/api/jobs/`
`title`, `location`, `company`, `job_type`, `category`, `salary_min`, `salary_max`

---

## Running Tests

```bash
docker compose exec web pytest
```

---

## User Roles

| Role | Permissions |
|---|---|
| `employer` | Post / edit / delete own jobs, view & update applicant status |
| `job_seeker` | Browse jobs, apply (once per job), track own applications |
