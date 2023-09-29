from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Count

from .forms import *


'''                 ****    Movie   ****                   '''


class SidebarData:
    @classmethod
    def get_genres(cls):
        return Genre.objects.annotate(movies_count=Count('movies'))

    @classmethod
    def get_movies(cls):
        return Movie.objects.all()

    @classmethod
    def get_years(cls):
        return cls.get_movies().values('year').order_by('-year')


class MovieListView(SidebarData, ListView):
    model = Movie
    template_name = 'mainapp/movie/movies_list.html'
    context_object_name = 'movies'
    paginate_by = 9

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Django Movies'

        return context

    @classmethod
    def get_queryset(cls):
        return SidebarData.get_movies().order_by('pk')


class FilterMoviesView(SidebarData, ListView):
    model = Movie
    template_name = 'mainapp/movie/filter_movies_list.html'
    context_object_name = 'movies'

    def get_queryset(self):
        queryset = SidebarData.get_movies()

        query = self.request.GET.get('movie-search')
        years = self.request.GET.getlist('year')
        genres = self.request.GET.getlist('genre')
        search_mode = self.request.GET.get('search-mode')

        if self.request.method == 'GET':
            if query is not None:
                queryset = queryset.filter(title__icontains=query)
            if years:
                queryset = queryset.filter(year__in=years)
            if genres:
                queryset = queryset.filter(genres__in=genres)
            if search_mode:
                queryset = queryset.order_by(self.request.GET.get('search-mode'))

        return queryset


class AboutMovieView(SidebarData, DetailView):
    model = Movie
    template_name = 'mainapp/movie/about_movie.html'
    context_object_name = 'movie'
    slug_url_kwarg = 'movie_slug'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.movie = self.get_object()
                new_comment.author = request.user
                new_comment.save()

                return redirect(self.get_object().get_absolute_url())
        else:
            comment_form = CommentForm()

        return reverse_lazy('about_movie', kwargs={'movie_slug': self.get_object().slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = CommentForm()
        context['comments'] = self.object.comments.order_by('-create_time')

        return context


class AddMovieView(SidebarData, LoginRequiredMixin, CreateView):
    form_class = MovieForm
    template_name = 'mainapp/movie/add_movie.html'
    context_object_name = 'form'
    login_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add movie'

        return context

    def get_success_url(self):
        return reverse_lazy('about_movie', kwargs={'movie_slug': self.object.slug})


class UpdateMovieView(SidebarData, LoginRequiredMixin, UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = 'mainapp/movie/update_movie.html'
    login_url = reverse_lazy('home')
    slug_url_kwarg = 'movie_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update movie'

        return context

    def get_success_url(self):
        return reverse_lazy('about_movie', kwargs={'movie_slug': self.object.slug})


class DeleteMovieView(SidebarData, LoginRequiredMixin, DeleteView):
    model = Movie
    login_url = reverse_lazy('home')
    success_url = reverse_lazy('home')
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


class AddActorView(SidebarData, LoginRequiredMixin, CreateView):
    form_class = ActorForm
    template_name = 'mainapp/person/add_person.html'
    context_object_name = 'form'
    login_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add actor'
        context['form_action'] = '/add_actor/'

        return context

    def get_success_url(self):
        return reverse_lazy('about_actor', kwargs={'actor_slug': self.object.slug})


class UpdateActorView(SidebarData, LoginRequiredMixin, UpdateView):
    model = Actor
    form_class = ActorForm
    template_name = 'mainapp/person/update_person.html'
    login_url = reverse_lazy('home')
    slug_url_kwarg = 'actor_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update actor'

        return context

    def get_success_url(self):
        return reverse_lazy('about_actor', kwargs={'actor_slug': self.object.slug})


class DeleteActorView(SidebarData, LoginRequiredMixin, DeleteView):
    model = Actor
    login_url = reverse_lazy('home')
    success_url = reverse_lazy('home')
    slug_url_kwarg = 'actor_slug'


'''                 ****    Director   ****                   '''


class AboutDirectorView(AboutActorView):
    model = Director
    slug_url_kwarg = 'director_slug'


class AddDirectorView(AddActorView):
    form_class = DirectorForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add director'
        context['form_action'] = '/add_director/'

        return context

    def get_success_url(self):
        return reverse_lazy('about_director', kwargs={'director_slug': self.object.slug})


class UpdateDirectorView(UpdateActorView):
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
        context['title'] = 'Genre ' + Genre.objects.get(slug=self.kwargs['genre_slug']).name

        return context

    def get_queryset(self):
        return Movie.objects.filter(genres__slug=self.kwargs['genre_slug']).order_by('create_time')


class AddGenreView(SidebarData, LoginRequiredMixin, CreateView):
    form_class = GenreForm
    template_name = 'mainapp/genre/add_genre.html'
    context_object_name = 'form'
    login_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add genre'

        return context

    def get_success_url(self):
        return reverse_lazy('genre', kwargs={'genre_slug': self.object.slug})


'''                 ****    Comment   ****                   '''


class UpdateCommentView(SidebarData, LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'mainapp/comment/update_comment.html'
    context_object_name = 'form'
    login_url = reverse_lazy('home')
    pk_url_kwarg = 'comment_id'
    slug_url_kwarg = 'movie_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update comment'

        return context

    def get_success_url(self):
        return reverse_lazy('about_movie', kwargs={'movie_slug': self.object.movie.slug})


class DeleteCommentView(SidebarData, LoginRequiredMixin, DeleteView):
    model = Comment
    login_url = reverse_lazy('home')
    success_url = reverse_lazy('home')
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


'''                 ****    Saga   ****                   '''


class AddSagaView(SidebarData, LoginRequiredMixin, CreateView):
    form_class = SagaForm
    template_name = 'mainapp/saga/add_saga.html'
    context_object_name = 'form'
    login_url = reverse_lazy('home')
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add saga'

        return context
