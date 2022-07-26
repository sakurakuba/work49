from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.forms import ModelMultipleChoiceField

from .models import Issue, Type, Status, Project


class IssueForm(forms.ModelForm):
    # summary = forms.CharField(max_length=50, required=True, label='Summary')
    # description = forms.CharField(max_length=300, required=False, label='Description')
    # type = forms.ModelMultipleChoiceField(queryset=Type.objects.all(), label='Type')
    # status = forms.ModelChoiceField(queryset=Status.objects.all(), label='Status')

    class Meta:
        model = Issue
        fields = "__all__"
        widgets = {
            "type": widgets.CheckboxSelectMultiple,
            "description": widgets.Textarea(attrs={"placeholder": "please add text here"})
        }

    def clean_summary(self):
        summary = self.cleaned_data.get('summary')
        if len(summary) > 20:
            raise ValidationError("Summary too long")
        return summary


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='Search')


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["project_name", "project_description", "start_date", "end_date"]
