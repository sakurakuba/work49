from django.forms import forms
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views import View
from django.views.generic import TemplateView

from issueTracker.forms import IssueForm
from issueTracker.models import Issue, Type, Status


class IndexView(View):
    def get(self, request, *args, **kwargs):
        issues = Issue.objects.order_by('-created_at')
        context = {'issues': issues}
        return render(request, "index.html", context)


class IssueView(TemplateView):
    template_name = 'issue_view.html'

    def get_context_data(self, **kwargs):
        pk = kwargs.get("pk")
        issue = get_object_or_404(Issue, pk=pk)
        kwargs["issue"] = issue
        return super().get_context_data(**kwargs)


class IssueCreate(View):
    def get(self, request, *args, **kwargs):
        form = IssueForm(data=request.GET)
        return render(request, "create.html", {'form': form})

    def post(self, request, *args, **kwargs):
        form = IssueForm(data=request.POST)
        if form.is_valid():
            summary = form.cleaned_data.get('summary')
            description = form.cleaned_data.get('description')
            status = form.cleaned_data.get('status')
            type = form.cleaned_data.pop('type')
            new_issue = Issue.objects.create(summary=summary, description=description, status=status)
            new_issue.type.set(type)
            return redirect('issue_view', pk=new_issue.pk)
        return render(request, 'create.html', {'form': form})


class IssueUpdate(View):
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        self.issue = get_object_or_404(Issue, pk=pk)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            form = IssueForm(initial={
                "summary": self.issue.summary,
                "description": self.issue.description,
                "status": self.issue.status,
                "type": self.issue.type.all()
            })
            return render(request, 'update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = IssueForm(data=request.POST)
        if form.is_valid():
            self.issue.summary = form.cleaned_data.get('summary')
            self.issue.description = form.cleaned_data.get('description')
            self.issue.status = form.cleaned_data.get('status')
            self.issue.type.set(form.cleaned_data.get('type'))
            self.issue.save()
            return redirect('issue_view', pk=kwargs.get("pk"))
        return render(request, 'update.html', {'form': form})


class IssueDelete(View):
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        self.issue = get_object_or_404(Issue, pk=pk)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {'issue': self.issue}
        return render(request, "delete.html", context)

    def post(self, request, *args, **kwargs):
        self.issue.delete()
        return redirect('index')
