from django import forms
from .models import Personnel


class PersonnelForm(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = [
            'full_name', 'identifier', 'birth_date', 'birth_place', 'engagement_basis',
            'employment_type', 'hire_date', 'contract_details', 'position', 'functions',
            'education', 'experience_summary', 'status', 'note'
        ]
        widgets = {
            'engagement_basis': forms.Textarea(attrs={'rows': 2}),
            'contract_details': forms.Textarea(attrs={'rows': 2}),
            'functions': forms.Textarea(attrs={'rows': 3}),
            'education': forms.Textarea(attrs={'rows': 3}),
            'experience_summary': forms.Textarea(attrs={'rows': 3}),
            'note': forms.Textarea(attrs={'rows': 2}),
        }
