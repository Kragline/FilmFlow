from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import CustomProfile


class CustomProfileInline(admin.StackedInline):
    model = CustomProfile
    can_delete = False
    verbose_name_plural = 'Custom profiles'


class UserAdmin(BaseUserAdmin):
    inlines = [CustomProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
