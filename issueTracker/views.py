from django.forms import forms
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, FormView

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


class IssueCreate(FormView):
    template_name = 'create.html'
    form_class = IssueForm

    def get_success_url(self):
        return reverse('issue_view', kwargs={'pk': self.issue.pk})

    def get(self, request):
        form = self.form_class()
        context = self.get_context(form=form)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_context(self, **kwargs):
        return kwargs

    def form_valid(self, form):
        self.issue = form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context(form=form)
        return render(self.request, self.template_name, context)


class IssueUpdate(FormView):
        template_name = 'update.html'
        form_class = IssueForm

        def dispatch(self, request, *args, **kwargs):
            self.issue = self.get_object()
            return super().dispatch(request, *args, **kwargs)

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['issue'] = self.issue
            return context

        def get_form_kwargs(self):
            kwargs = super().get_form_kwargs()
            kwargs['instance'] = self.issue
            return kwargs

        def form_valid(self, form):
            self.issue = form.save()
            return super().form_valid(form)

        def get_success_url(self):
            return reverse('issue_view', kwargs={'pk': self.issue.pk})

        def get_object(self):
            pk = self.kwargs.get('pk')
            return get_object_or_404(Issue, pk=pk)


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
