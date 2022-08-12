
from django.urls import path

from issueTracker.views import IndexView, IssueView, IssueUpdate, IssueCreate, IssueDelete, AllProjectsView, \
    ProjectView, ProjectCreate, ProjectUpdate, ProjectDelete, UserAdd, UserDelete

app_name = "issueTracker"

urlpatterns = [
    path('', AllProjectsView.as_view(), name="index"),
    path('project/<int:pk>/', ProjectView.as_view(), name="project_view"),
    path('project/<int:pk>/update', ProjectUpdate.as_view(), name="project_update"),
    path('project/<int:pk>/delete', ProjectDelete.as_view(), name="project_delete"),
    path('project/create/', ProjectCreate.as_view(), name="project_create"),
    path('issues/', IndexView.as_view(), name="issues"),
    path('issue/<int:pk>/', IssueView.as_view(), name="issue_view"),
    path('issue/<int:pk>/update/', IssueUpdate.as_view(), name="update"),
    path('issue/<int:pk>/delete/', IssueDelete.as_view(), name="delete"),
    path('project/<int:pk>/issue/create/', IssueCreate.as_view(), name="create"),
    path('project/<int:pk>/user/add', UserAdd.as_view(), name="user_add"),
    path('users/<int:pk>/delete', UserDelete.as_view(), name="user_delete"),
]
