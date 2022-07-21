from django.db.models import Q
from django.forms import forms
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse
from django.utils.http import urlencode
from django.views import View
from django.views.generic import TemplateView, FormView, ListView

from issueTracker.forms import IssueForm, SearchForm
from issueTracker.models import Issue, Type, Status


# class IndexView(View):
#     def get(self, request, *args, **kwargs):
#         issues = Issue.objects.order_by('-created_at')
#         context = {'issues': issues}
#         return render(request, "index.html", context)

class IndexView(ListView):
    model = Issue
    template_name = "index.html"
    context_object_name = "issues"
    ordering = ["-created_at"]
    paginate_by = 8

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Issue.objects.filter(Q(summary__contains=self.search_value) | Q(description__contains=self.search_value))
        return Issue.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            val = urlencode({'search': self.search_value})
            context['query'] = val
            context['search'] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")


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
