from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class ActorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_html_photo', 'create_time')
    list_display_links = ('id', 'name')

    search_fields = ('name',)
    list_filter = ('create_time',)
    prepopulated_fields = {'slug': ('name',)}

    save_on_top = True

    def get_html_photo(self, model_object):
        if model_object.photo:
            return mark_safe(f'<img src="{model_object.photo.url}" width=70">')

    get_html_photo.short_description = 'Photo'


class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_html_photo', 'create_time', 'rating')
    list_display_links = ('id', 'title', 'rating')

    search_fields = ('title',)
    list_filter = ('create_time',)
    prepopulated_fields = {'slug': ('title',)}

    save_on_top = True

    def get_html_photo(self, model_object):
        if model_object.poster:
            return mark_safe(f'<img src="{model_object.poster.url}" width=70">')

    get_html_photo.short_description = 'Poster'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class SagaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

    search_fields = ('name',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'movie', 'text')
    list_display_links = ('author', 'movie', 'text')


class TroubleshootAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'user', 'get_user_photo')
    list_display_links = ('id', 'category')

    def get_user_photo(self, model_object):
        if model_object.user.custom_profile.profile_pic:
            return mark_safe(f'<img src="{model_object.user.custom_profile.profile_pic.url}" width=70">')

    get_user_photo.short_description = 'Profile pic'


admin.site.register(Actor, ActorAdmin)
admin.site.register(Director, ActorAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Saga, SagaAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Troubleshoot, TroubleshootAdmin)

admin.site.site_title = 'FilmFlow Administration'
admin.site.site_header = 'FilmFlow Administration'
