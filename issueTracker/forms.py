from django import forms
from django.forms import ModelMultipleChoiceField

from .models import Issue, Type, Status


class IssueForm(forms.ModelForm):
    summary = forms.CharField(max_length=50, required=True, label='Summary')
    description = forms.CharField(max_length=300, required=False, label='Description')
    type = forms.ModelMultipleChoiceField(queryset=Type.objects.all(), label='Type')
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label='Status')

    class Meta:
        model = Issue
        fields = "__all__"
