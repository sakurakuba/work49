"""djangoProject49 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from issueTracker.views import IndexView, IssueView, IssueUpdate, IssueCreate, IssueDelete, AllProjectsView, \
    ProjectView, ProjectCreate


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name="index"),
    path('issue/<int:pk>/', IssueView.as_view(), name="issue_view"),
    path('issue/<int:pk>/update/', IssueUpdate.as_view(), name="update"),
    path('issue/<int:pk>/delete/', IssueDelete.as_view(), name="delete"),
    path('issue/create/', IssueCreate.as_view(), name="create"),
    path('allprojects/', AllProjectsView.as_view(), name="all_projects_view"),
    path('project/<int:pk>/', ProjectView.as_view(), name="project_view"),
    path('project/create/', ProjectCreate.as_view(), name="project_create"),
]
