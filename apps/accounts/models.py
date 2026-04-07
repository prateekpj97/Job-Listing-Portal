from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    EMPLOYER = 'employer'
    JOB_SEEKER = 'job_seeker'
    ROLE_CHOICES = [(EMPLOYER, 'Employer'), (JOB_SEEKER, 'Job Seeker')]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=JOB_SEEKER)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True)
    company_website = models.URLField(blank=True)

    def is_employer(self):
        return self.role == self.EMPLOYER

    def is_job_seeker(self):
        return self.role == self.JOB_SEEKER

    class Meta:
        verbose_name = 'User'
