from django.contrib import admin

# Register your models here.
from issueTracker.models import Issue, Status, Type, Project


class IssueAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary', 'status', 'get_types', 'created_at']
    list_display_links = ['summary']
    list_filter = ['status']
    search_fields = ['summary', 'status']
    fields = ['summary', 'description', 'status', 'type', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']

    def get_types(self, obj):
        return "\n".join([t.name for t in obj.type.all()])


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'project_name', 'start_date', 'end_date', 'created_at']
    list_display_links = ['project_name']
    list_filter = ['project_name']
    search_fields = ['project_name']
    fields = ['project_name', 'project_description', 'start_date', 'end_date', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Issue, IssueAdmin)
admin.site.register(Project, ProjectAdmin)
