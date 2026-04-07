from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.jobs.models import Job
from apps.jobs.tasks import notify_employer_new_application, notify_applicant_status_change
from .models import Application
from .forms import ApplicationForm, ApplicationStatusForm

@login_required
def apply(request, job_pk):
    job = get_object_or_404(Job, pk=job_pk, is_active=True)
    if request.user.is_employer():
        messages.error(request, 'Employers cannot apply for jobs.')
        return redirect('job_detail', pk=job_pk)
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', pk=job_pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.job = job
            app.applicant = request.user
            app.save()
            notify_employer_new_application.delay(
                job.title, job.posted_by.email, request.user.get_full_name() or request.user.username)
            messages.success(request, 'Application submitted!')
            return redirect('my_applications')
    else:
        form = ApplicationForm()
    return render(request, 'applications/apply.html', {'form': form, 'job': job})

@login_required
def my_applications(request):
    apps = Application.objects.filter(applicant=request.user).select_related('job', 'job__posted_by')
    return render(request, 'applications/my_applications.html', {'applications': apps})

@login_required
def job_applications(request, job_pk):
    job = get_object_or_404(Job, pk=job_pk, posted_by=request.user)
    apps = job.applications.select_related('applicant')
    return render(request, 'applications/job_applications.html', {'job': job, 'applications': apps})

@login_required
def update_status(request, pk):
    app = get_object_or_404(Application, pk=pk, job__posted_by=request.user)
    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST, instance=app)
        if form.is_valid():
            form.save()
            notify_applicant_status_change.delay(app.job.title, app.applicant.email, app.status)
            messages.success(request, 'Status updated.')
            return redirect('job_applications', job_pk=app.job.pk)
    else:
        form = ApplicationStatusForm(instance=app)
    return render(request, 'applications/update_status.html', {'form': form, 'application': app})
