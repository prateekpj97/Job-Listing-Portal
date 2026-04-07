import pytest
from django.urls import reverse
from apps.applications.models import Application

@pytest.mark.django_db
class TestApplicationModel:
    def test_application_str(self, application):
        assert 'seeker1' in str(application)
        assert 'Senior Django Developer' in str(application)

    def test_unique_application(self, job, job_seeker):
        Application.objects.create(job=job, applicant=job_seeker, cover_letter='First')
        with pytest.raises(Exception):
            Application.objects.create(job=job, applicant=job_seeker, cover_letter='Second')

@pytest.mark.django_db
class TestApplicationViews:
    def test_apply_requires_login(self, client, job):
        response = client.get(reverse('apply', args=[job.pk]))
        assert response.status_code == 302
        assert '/accounts/login/' in response['Location']

    def test_job_seeker_can_apply(self, client, job_seeker, job):
        client.login(username='seeker1', password='testpass123')
        response = client.post(reverse('apply', args=[job.pk]), {
            'cover_letter': 'I am perfect for this role!'
        })
        assert response.status_code == 302
        assert Application.objects.filter(job=job, applicant=job_seeker).exists()

    def test_employer_cannot_apply(self, client, employer, job):
        client.login(username='employer1', password='testpass123')
        response = client.post(reverse('apply', args=[job.pk]), {
            'cover_letter': 'Employer applying'
        })
        assert response.status_code == 302
        assert not Application.objects.filter(applicant=employer).exists()

    def test_cannot_apply_twice(self, client, job_seeker, job, application):
        client.login(username='seeker1', password='testpass123')
        response = client.post(reverse('apply', args=[job.pk]), {
            'cover_letter': 'Second attempt'
        })
        assert response.status_code == 302
        assert Application.objects.filter(job=job, applicant=job_seeker).count() == 1

    def test_my_applications(self, client, job_seeker, application):
        client.login(username='seeker1', password='testpass123')
        response = client.get(reverse('my_applications'))
        assert response.status_code == 200
        assert b'Senior Django Developer' in response.content

    def test_job_applications_view_employer(self, client, employer, job, application):
        client.login(username='employer1', password='testpass123')
        response = client.get(reverse('job_applications', args=[job.pk]))
        assert response.status_code == 200
        assert b'seeker1' in response.content

    def test_update_status_by_employer(self, client, employer, application):
        client.login(username='employer1', password='testpass123')
        response = client.post(reverse('update_status', args=[application.pk]), {
            'status': Application.ACCEPTED
        })
        assert response.status_code == 302
        application.refresh_from_db()
        assert application.status == Application.ACCEPTED

    def test_application_status_default_pending(self, application):
        assert application.status == Application.PENDING

@pytest.mark.django_db
class TestApplicationAPI:
    def test_api_applications_requires_auth(self, client):
        response = client.get('/api/applications/')
        assert response.status_code == 403

    def test_seeker_sees_own_applications(self, client, job_seeker, application):
        client.login(username='seeker1', password='testpass123')
        response = client.get('/api/applications/')
        assert response.status_code == 200
        data = response.json()
        assert data['count'] == 1
