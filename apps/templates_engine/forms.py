from django import forms
from .models import Template, TemplateVersion


class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ['name', 'module', 'is_active']


class TemplateVersionForm(forms.ModelForm):
    class Meta:
        model = TemplateVersion
        fields = ['version', 'file', 'file_format', 'placeholder_schema', 'is_active']
