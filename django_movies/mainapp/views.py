from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.views.generic import View, ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.db.models import Q
from .models import Rating
from .forms import *
import json

from utils.utils_data import SidebarData, AddObjectView, UpdateObjectView, DeleteObjectView, get_avg_rating


'''                 ****    Movie   ****                   '''


class MovieListView(SidebarData, ListView):
    model = Movie
    template_name = 'mainapp/movie/movies_list.html'
    context_object_name = 'movies'
    context_title = 'Select your favorite'
    paginate_by = 9

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.context_title
        context['title'] = 'FilmFlow - Online cinema'

        return context
    
    def search_by_query(self, search_query: str, queryset: QuerySet[Movie]) -> QuerySet[Movie]:
        keywords = [word for word in search_query.split() if len(word) > 2]
        q_objects = Q()

        for keyword in keywords:
            q_objects |= Q(title__icontains=keyword)

        return queryset.filter(q_objects)

    def get_queryset(self):
        queryset = SidebarData.ALL_MOVIES.order_by('id')

        if self.request.method == 'GET':
            if query := self.request.GET.get('movie-search'):
                queryset = self.search_by_query(query, queryset)

            if years := self.request.GET.getlist('year'):
                queryset = queryset.filter(year__in=years)

            if countries := self.request.GET.getlist('country'):
                queryset = queryset.filter(country__in=countries)

            if not queryset.exists():
                self.context_title = 'No matches found'

        return queryset.distinct()


class AboutMovieView(SidebarData, DetailView):
    model = Movie
    template_name = 'mainapp/movie/about_movie.html'
    context_object_name = 'movie'
    slug_url_kwarg = 'movie_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if movie_saga:=self.object.saga:
            context['other_movies'] = SidebarData.ALL_MOVIES.filter(saga=movie_saga).order_by('world_premiere')

        context['title'] = 'Watch ' + self.object.title + ' online'
        context['movie_actors'] = self.object.actors.order_by('name')

        context['recomendations'] = SidebarData.ALL_MOVIES.filter(genres__in=SidebarData.NOT_EMPTY_GENRES).order_by('?').distinct()[:15]

        context['form'] = CommentForm()
        context['comments'] = self.object.comments.order_by('-create_time')

        current_user = self.request.user
        context['current_user'] = current_user

        if movie_ratings:=Rating.objects.filter(movie=self.object):
            context['rated'] = True
            context['avg_rating'] = get_avg_rating(movie_ratings)

        return context


class RateMovieView(SidebarData, LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        rating_score = int(request.POST.get('rating_score'))
        rated_movie = SidebarData.ALL_MOVIES.get(id=request.POST.get('movie_id'))

        rating, created = Rating.objects.update_or_create(
            movie=rated_movie,
            user=request.user, defaults={
                'score': rating_score
            })
        
        return JsonResponse({'newAvgRating': get_avg_rating(Rating.objects.filter(movie=rated_movie))})

    def get(self, request, *args, **kwargs):
        return redirect('home')


class AddMovieView(AddObjectView):
    form_class = MovieForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add movie'
        context['form_action'] = '/movie/add/'

        return context

    def get_success_url(self):
        return reverse_lazy('about_movie', kwargs={'movie_slug': self.object.slug})


class UpdateMovieView(UpdateObjectView):
    model = Movie
    form_class = MovieForm
    slug_url_kwarg = 'movie_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update movie'

        return context

    def get_success_url(self):
        return reverse_lazy('about_movie', kwargs={'movie_slug': self.object.slug})


class DeleteMovieView(DeleteObjectView):
    model = Movie
    slug_url_kwarg = 'movie_slug'


'''                 ****    Actor   ****                   '''


class AboutActorView(SidebarData, DetailView):
    model = Actor
    template_name = 'mainapp/person/about_person.html'
    context_object_name = 'person'
    slug_url_kwarg = 'actor_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'About ' + str(context['person'].name)

        return context


class AddActorView(AddObjectView):
    form_class = ActorForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add actor'
        context['form_action'] = '/actor/add/'

        return context

    def get_success_url(self):
        return reverse_lazy('about_actor', kwargs={'actor_slug': self.object.slug})


class UpdateActorView(UpdateObjectView):
    model = Actor
    form_class = ActorForm
    slug_url_kwarg = 'actor_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update actor'

        return context

    def get_success_url(self):
        return reverse_lazy('about_actor', kwargs={'actor_slug': self.object.slug})


class DeleteActorView(DeleteObjectView):
    model = Actor
    slug_url_kwarg = 'actor_slug'


'''                 ****    Director   ****                   '''


class AboutDirectorView(AboutActorView):
    model = Director
    slug_url_kwarg = 'director_slug'


class AddDirectorView(AddObjectView):
    form_class = DirectorForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add director'
        context['form_action'] = '/director/add/'

        return context

    def get_success_url(self):
        return reverse_lazy('about_director', kwargs={'director_slug': self.object.slug})


class UpdateDirectorView(UpdateObjectView):
    model = Director
    form_class = DirectorForm
    slug_url_kwarg = 'director_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update director'

        return context

    def get_success_url(self):
        return reverse_lazy('about_director', kwargs={'director_slug': self.object.slug})


class DeleteDirectorView(DeleteActorView):
    model = Director
    slug_url_kwarg = 'director_slug'


'''                 ****    Genre   ****                   '''


class GenreListView(SidebarData, ListView):
    model = Movie
    template_name = 'mainapp/genre/show_genre.html'
    context_object_name = 'movies'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Genre.objects.get(slug=self.kwargs['genre_slug']).name + ' Movies'

        return context

    def get_queryset(self):
        return Movie.objects.filter(genres__slug=self.kwargs['genre_slug']).order_by('create_time')


class AddGenreView(AddObjectView):
    form_class = GenreForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add genre'
        context['form_action'] = '/movie/genre/add/'

        return context

    def get_success_url(self):
        return reverse_lazy('genre', kwargs={'genre_slug': self.object.slug})


'''                 ****    Comment   ****                   '''


class AddCommentView(SidebarData, LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                commented_movie = SidebarData.ALL_MOVIES.get(id=request.POST.get('movie_id'))

                new_comment = comment_form.save(commit=False)
                new_comment.movie = commented_movie
                new_comment.author = request.user
                new_comment.save()

            return redirect(commented_movie.get_absolute_url())
        else:
            comment_form = CommentForm()

        return reverse_lazy('about_movie', kwargs={'movie_slug': commented_movie.slug})


class UpdateCommentView(UpdateObjectView):
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'
    slug_url_kwarg = 'movie_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update comment'

        return context

    def get_success_url(self):
        return reverse_lazy('about_movie', kwargs={'movie_slug': self.object.movie.slug})


class DeleteCommentView(DeleteObjectView):
    model = Comment
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse_lazy('about_movie', kwargs={'movie_slug': self.object.movie.slug})


class LikeCommentView(SidebarData, LoginRequiredMixin, View):
    def post(self, request, movie_slug, comment_id, *args, **kwargs):
        movie = Movie.objects.get(slug=movie_slug)
        comment = movie.comments.get(pk=comment_id)
        current_user = self.request.user

        if current_user in comment.likes.all():
            comment.likes.remove(current_user)
        else:
            comment.likes.add(current_user)

        return redirect(movie.get_absolute_url())


'''                 ****    Other   ****                   '''


class AboutUsView(SidebarData, TemplateView):
    template_name = 'mainapp/other/about_us.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'About FilmFlow'

        return context


class ContactsView(SidebarData, TemplateView):
    template_name = 'mainapp/other/contacts.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Contacts'

        return context


class TroubleshootView(AddObjectView):
    form_class = TroubleshootForm
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        trouble = form.save(commit=False)
        trouble.user = self.request.user
        trouble.save()

        return redirect('home')

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Tell about your problem'
        context['form_action'] = '/troubleshoot/'

        return context
