from django.db.models import Count
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView

from mainapp.models import Genre, Movie


class SidebarData():
    @classmethod
    def not_empty_genres(cls):
        return list(enumerate(Genre.objects.annotate(movies_count=Count('movies')).filter(movies_count__gt=0), start=1))

    @classmethod
    def all_movies(cls):
        return Movie.objects.all()
    
    @classmethod
    def all_years(cls):
        return list(enumerate(cls.all_movies().values('year').order_by('-year').distinct(), start=1))
    
    @classmethod
    def all_countries(cls):
        return list(enumerate(cls.all_movies().values('country').order_by().distinct(), start=1))
    
    @classmethod
    def latest_premieres(cls):
        return cls.all_movies().order_by('-world_premiere')[:4]
    
    @classmethod
    def recently_added(cls):
        return cls.all_movies().order_by('-pk')[:10]


class BaseObjectView(SidebarData, LoginRequiredMixin):
    login_url = reverse_lazy('home')
    template_name = 'mainapp/add_update_object.html'
    context_object_name = 'form'


class AddObjectView(BaseObjectView, CreateView):
    pass


class UpdateObjectView(BaseObjectView, UpdateView):
    pass


class DeleteObjectView(BaseObjectView, DeleteView):
    success_url = reverse_lazy('home')


def get_avg_rating(queryset):
        rating_sum = 0
        for rating in queryset:
            rating_sum += rating.score

        return round(rating_sum / len(queryset), 1)
