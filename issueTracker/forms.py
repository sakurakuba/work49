from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.forms import ModelMultipleChoiceField

from .models import Issue, Type, Status, Project


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ["summary", "description", "status", "type"]
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


class UserAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        pk = kwargs.pop("pk")
        super().__init__(*args, **kwargs)
        self.fields['users'].queryset = get_user_model().objects.exclude(pk=pk)

    class Meta:
        model = Project
        fields = ("users",)
        widget = {"users": widgets.CheckboxSelectMultiple}




