from django import forms
from .models import Issue, Type, Status


class IssueForm(forms.ModelForm):
    summary = forms.CharField(max_length=50, required=True, label='summary')
    description = forms.CharField(max_length=300, required=False, label='description')
    type = forms.ModelChoiceField(queryset=Type.objects.all(), label='type')
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label='status')

    class Meta:
        model = Issue
        fields = "__all__"
