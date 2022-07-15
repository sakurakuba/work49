from django.contrib import admin

# Register your models here.
from issueTracker.models import Issue, Status, Type


class IssueAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary', 'status', 'type', 'created_at']
    list_display_links = ['summary']
    list_filter = ['status']
    search_fields = ['summary', 'status']
    fields = ['summary', 'description', 'status', 'type', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Issue, IssueAdmin)
