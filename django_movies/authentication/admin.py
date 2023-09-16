from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe

from .models import CustomProfile


class CustomProfileInline(admin.StackedInline):
    model = CustomProfile
    can_delete = False
    verbose_name_plural = 'Custom profiles'


class UserAdmin(BaseUserAdmin):
    inlines = [CustomProfileInline]
    save_on_top = True

    list_display = ('id', 'username', 'first_name', 'last_name', 'get_html_photo', 'is_staff')
    list_display_links = ('id', 'username', 'first_name', 'last_name')
    ordering = ('-id',)

    search_fields = ('username', 'first_name', 'last_name')

    def get_html_photo(self, model_object):
        if model_object.custom_profile.profile_pic:
            return mark_safe(f'<img src="{model_object.custom_profile.profile_pic.url}" width=70">')

    get_html_photo.short_description = 'Profile pic'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
