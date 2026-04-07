from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
from .models import Job, Category
from .forms import JobForm
from .filters import JobFilter

def job_list(request):
    cache_key = f'job_list_{request.GET.urlencode()}'
    jobs = cache.get(cache_key)
    if not jobs:
        qs = Job.objects.filter(is_active=True).select_related('category', 'posted_by')
        f = JobFilter(request.GET, queryset=qs)
        jobs = f.qs
        cache.set(cache_key, jobs, 60)
    else:
        f = JobFilter(request.GET, queryset=jobs)
    categories = Category.objects.all()
    return render(request, 'jobs/job_list.html', {'filter': f, 'categories': categories})

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    user_applied = False
    if request.user.is_authenticated:
        user_applied = job.applications.filter(applicant=request.user).exists()
    return render(request, 'jobs/job_detail.html', {'job': job, 'user_applied': user_applied})

@login_required
def job_create(request):
    if not request.user.is_employer():
        messages.error(request, 'Only employers can post jobs.')
        return redirect('job_list')
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            cache.clear()
            messages.success(request, 'Job posted successfully!')
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm()
    return render(request, 'jobs/job_form.html', {'form': form, 'action': 'Post'})

@login_required
def job_edit(request, pk):
    job = get_object_or_404(Job, pk=pk, posted_by=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            cache.clear()
            messages.success(request, 'Job updated.')
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/job_form.html', {'form': form, 'action': 'Edit', 'job': job})

@login_required
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk, posted_by=request.user)
    if request.method == 'POST':
        job.delete()
        cache.clear()
        messages.success(request, 'Job deleted.')
        return redirect('my_jobs')
    return render(request, 'jobs/job_confirm_delete.html', {'job': job})

@login_required
def my_jobs(request):
    if not request.user.is_employer():
        return redirect('job_list')
    jobs = Job.objects.filter(posted_by=request.user).prefetch_related('applications')
    return render(request, 'jobs/my_jobs.html', {'jobs': jobs})
