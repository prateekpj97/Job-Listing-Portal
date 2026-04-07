from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('title', 'description', 'requirements', 'company', 'location',
                  'salary_min', 'salary_max', 'job_type', 'category', 'deadline', 'is_active')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }
