from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('cover_letter', 'resume')
        widgets = {'cover_letter': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Tell us why you are a great fit...'})}

class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('status',)
