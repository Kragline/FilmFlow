from django.db.models import Count
from .models import *


class DataMixin:
    paginate_by = 9

    @classmethod
    def get_genres(cls):
        return Genre.objects.annotate(movies_count=Count('movies'))

    def get_user_context(self, **kwargs):
        categories = self.get_genres()

        context = kwargs
        context['genres'] = categories

        return context
