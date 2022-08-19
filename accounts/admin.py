from django.contrib import admin
from django.contrib.auth import get_user_model
from accounts.models import Profile


class ProfileInLine(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    inlines = (ProfileInLine,)


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserAdmin)
