import pytest
from django.test import Client
from apps.accounts.models import User
from apps.jobs.models import Job, Category
from apps.applications.models import Application

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def employer(db):
    return User.objects.create_user(
        username='employer1', email='employer@test.com',
        password='testpass123', role=User.EMPLOYER,
        company_name='Test Corp')

@pytest.fixture
def job_seeker(db):
    return User.objects.create_user(
        username='seeker1', email='seeker@test.com',
        password='testpass123', role=User.JOB_SEEKER)

@pytest.fixture
def category(db):
    return Category.objects.create(name='Engineering', slug='engineering')

@pytest.fixture
def job(db, employer, category):
    return Job.objects.create(
        title='Senior Django Developer',
        description='Build awesome Django apps.',
        requirements='3+ years experience',
        company='Test Corp',
        location='Remote',
        salary_min=80000,
        salary_max=120000,
        job_type=Job.FULL_TIME,
        category=category,
        posted_by=employer,
        is_active=True)

@pytest.fixture
def application(db, job, job_seeker):
    return Application.objects.create(
        job=job, applicant=job_seeker,
        cover_letter='I am a great fit!',
        status=Application.PENDING)
