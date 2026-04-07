import django_filters
from .models import Job, Category

class JobFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Search')
    location = django_filters.CharFilter(lookup_expr='icontains')
    company = django_filters.CharFilter(lookup_expr='icontains')
    salary_min = django_filters.NumberFilter(field_name='salary_min', lookup_expr='gte', label='Min Salary')
    salary_max = django_filters.NumberFilter(field_name='salary_max', lookup_expr='lte', label='Max Salary')
    job_type = django_filters.ChoiceFilter(choices=Job.JOB_TYPE_CHOICES)
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = Job
        fields = ['title', 'location', 'company', 'job_type', 'category', 'salary_min', 'salary_max']
