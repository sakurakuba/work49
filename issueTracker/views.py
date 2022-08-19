from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import forms
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views import View
from django.views.generic import TemplateView, FormView, ListView, DetailView, CreateView, UpdateView, DeleteView

from issueTracker.forms import IssueForm, SearchForm, ProjectForm, UserAddForm
from issueTracker.models import Issue, Type, Status, Project


#### Issue workflow

# class IndexView(View):
#     def get(self, request, *args, **kwargs):
#         issues = Issue.objects.order_by('-created_at')
#         context = {'issues': issues}
#         return render(request, "index.html", context)

class IndexView(LoginRequiredMixin, ListView):
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


class IssueView(PermissionRequiredMixin, DetailView):
    model = Issue
    template_name = 'issue_view.html'
    permission_required = "issueTracker.view_issue"

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().project.users.all() or self.request.user.is_superuser


class IssueCreate(PermissionRequiredMixin, CreateView):
    template_name = 'create.html'
    form_class = IssueForm
    permission_required = "issueTracker.add_issue"

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        form.instance.project = project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("issueTracker:project_view", kwargs={"pk": self.object.project.pk})


class IssueUpdate(PermissionRequiredMixin, UpdateView):
        template_name = 'update.html'
        form_class = IssueForm
        model = Issue
        permission_required = "issueTracker.change_issue"


class IssueDelete(PermissionRequiredMixin, DeleteView):
    model = Issue
    template_name = "delete.html"
    permission_required = "issueTracker.delete_issue"

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


class ProjectView(PermissionRequiredMixin, DetailView):
    template_name = 'project_view.html'
    model = Project
    permission_required = "issueTracker.view_project"

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        context['issues'] = self.object.projects.all().order_by('-created_at')
        u = self.request.user.groups.filter(name__in=['Project Manager', 'Team Lead']).exists()
        context['u'] = u
        return context

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().users.all() or self.request.user.is_superuser


class ProjectCreate(PermissionRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = "project_create.html"
    permission_required = "issueTracker.add_project"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.users.add(self.request.user)
        return response



class ProjectUpdate(PermissionRequiredMixin, UpdateView):
        template_name = 'project_update.html'
        form_class = ProjectForm
        model = Project
        permission_required = "issueTracker.change_project"

        def has_permission(self):
            return super().has_permission() and self.request.user in self.get_object().users.all() or self.request.user.is_superuser


class ProjectDelete(PermissionRequiredMixin, DeleteView):
    model = Project
    template_name = "project_delete.html"
    success_url = reverse_lazy("issueTracker:index")
    permission_required = "issueTracker.delete_project"

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().users.all() or self.request.user.is_superuser


class UserAdd(PermissionRequiredMixin, UpdateView):
    model = Project
    form_class = UserAddForm
    template_name = "users.html"
    permission_required = "issueTracker.add_users_to_project"
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["pk"] = self.request.user.pk
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.users.add(self.request.user)
        return response

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().users.all() or self.request.user.is_superuser

    def get_success_url(self):
        return reverse("issueTracker:project_view", kwargs={"pk": self.object.pk})


