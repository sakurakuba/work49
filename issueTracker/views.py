from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import forms
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views import View
from django.views.generic import TemplateView, FormView, ListView, DetailView, CreateView, UpdateView, DeleteView

from issueTracker.forms import IssueForm, SearchForm, ProjectForm, UserAddForm, UserDeleteForm
from issueTracker.models import Issue, Type, Status, Project


#### Issue workflow

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
        return Issue.objects.order_by("-created_at")

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


class IssueCreate(LoginRequiredMixin, CreateView):
    template_name = 'create.html'
    form_class = IssueForm

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        form.instance.project = project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("issueTracker:project_view", kwargs={"pk": self.object.project.pk})


class IssueUpdate(LoginRequiredMixin, UpdateView):
        template_name = 'update.html'
        form_class = IssueForm
        model = Issue


class IssueDelete(LoginRequiredMixin, DeleteView):
    model = Issue
    template_name = "delete.html"

    def get_success_url(self):
        return reverse("issueTracker:project_view", kwargs={"pk": self.object.project.pk})



##### Project workflow

class AllProjectsView(ListView):
    model = Project
    template_name = "allprojects.html"
    context_object_name = "projects"
    ordering = ["-created_at"]
    paginate_by = 8

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Project.objects.filter(Q(project_name__contains=self.search_value) | Q(project_description__contains=self.search_value))
        return Project.objects.order_by("-created_at")

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


class ProjectView(DetailView):
    template_name = 'project_view.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        context['issues'] = self.object.projects.all().order_by('-created_at')
        return context


class ProjectCreate(LoginRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = "project_create.html"


class UserAdd(LoginRequiredMixin, CreateView):
    form_class = UserAddForm
    template_name = "users.html"

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        user = form.save(commit=False)
        for u in project.users.all():
            u.set(user)
        return redirect("issueTracker:project_view", pk=project.pk)

    def get_success_url(self):
        return reverse("issueTracker:project_view", kwargs={"pk": self.object.project.pk})


class ProjectUpdate(LoginRequiredMixin, UpdateView):
        template_name = 'project_update.html'
        form_class = ProjectForm
        model = Project


class ProjectDelete(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = "project_delete.html"
    success_url = reverse_lazy("issueTracker:index")


# class UserDelete(DeleteView):
#     model = User
#     form_class = UserDeleteForm
#     template_name = "delete_users.html"
#
#     def get(self, request, *args, **kwargs):
#         user = self.request.user
#         return super().delete(request, *args, **kwargs)
#
#     def get_success_url(self):
#         return reverse("issueTracker:project_view", kwargs={"pk": self.object.pk})

def user_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    for u in project.users.all():
        u.delete()
    return reverse("issueTracker:index")
