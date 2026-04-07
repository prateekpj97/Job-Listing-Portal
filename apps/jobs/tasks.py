from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def notify_employer_new_application(job_title, employer_email, applicant_name):
    send_mail(
        subject=f'New Application: {job_title}',
        message=f'{applicant_name} has applied for your job posting: {job_title}.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[employer_email],
        fail_silently=True,
    )

@shared_task
def notify_applicant_status_change(job_title, applicant_email, status):
    send_mail(
        subject=f'Application Update: {job_title}',
        message=f'Your application for "{job_title}" has been {status}.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[applicant_email],
        fail_silently=True,
    )
