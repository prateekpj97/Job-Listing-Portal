import pytest
from django.urls import reverse
from apps.jobs.models import Job, Category

@pytest.mark.django_db
class TestJobModel:
    def test_job_str(self, job):
        assert str(job) == 'Senior Django Developer @ Test Corp'

    def test_job_defaults(self, job):
        assert job.is_active is True
        assert job.job_type == Job.FULL_TIME

    def test_category_str(self, category):
        assert str(category) == 'Engineering'

@pytest.mark.django_db
class TestJobViews:
    def test_job_list_anonymous(self, client, job):
        response = client.get(reverse('job_list'))
        assert response.status_code == 200
        assert b'Senior Django Developer' in response.content

    def test_job_detail(self, client, job):
        response = client.get(reverse('job_detail', args=[job.pk]))
        assert response.status_code == 200
        assert b'Test Corp' in response.content

    def test_job_create_requires_login(self, client):
        response = client.get(reverse('job_create'))
        assert response.status_code == 302
        assert '/accounts/login/' in response['Location']

    def test_employer_can_create_job(self, client, employer, category):
        client.login(username='employer1', password='testpass123')
        data = {
            'title': 'New Job', 'description': 'Great job', 'requirements': 'Python',
            'company': 'My Corp', 'location': 'NYC', 'job_type': Job.FULL_TIME,
            'is_active': True,
        }
        response = client.post(reverse('job_create'), data)
        assert response.status_code == 302
        assert Job.objects.filter(title='New Job').exists()

    def test_job_seeker_cannot_create_job(self, client, job_seeker):
        client.login(username='seeker1', password='testpass123')
        response = client.get(reverse('job_create'))
        assert response.status_code == 302

    def test_job_list_filter_by_type(self, client, job):
        response = client.get(reverse('job_list') + '?job_type=full_time')
        assert response.status_code == 200
        assert b'Senior Django Developer' in response.content

    def test_job_list_filter_by_location(self, client, job):
        response = client.get(reverse('job_list') + '?location=Remote')
        assert response.status_code == 200
        assert b'Senior Django Developer' in response.content

    def test_job_edit_by_owner(self, client, employer, job):
        client.login(username='employer1', password='testpass123')
        data = {
            'title': 'Updated Title', 'description': job.description,
            'requirements': job.requirements, 'company': job.company,
            'location': job.location, 'job_type': job.job_type, 'is_active': True,
        }
        response = client.post(reverse('job_edit', args=[job.pk]), data)
        assert response.status_code == 302
        job.refresh_from_db()
        assert job.title == 'Updated Title'

    def test_my_jobs_requires_employer(self, client, job_seeker):
        client.login(username='seeker1', password='testpass123')
        response = client.get(reverse('my_jobs'))
        assert response.status_code == 302

@pytest.mark.django_db
class TestJobAPI:
    def test_api_job_list(self, client, job):
        response = client.get('/api/jobs/')
        assert response.status_code == 200
        data = response.json()
        assert data['count'] >= 1

    def test_api_job_detail(self, client, job):
        response = client.get(f'/api/jobs/{job.pk}/')
        assert response.status_code == 200
        assert response.json()['title'] == 'Senior Django Developer'

    def test_api_job_filter_by_type(self, client, job):
        response = client.get('/api/jobs/?job_type=full_time')
        assert response.status_code == 200
        assert response.json()['count'] >= 1
