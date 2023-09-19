from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Count

from .forms import *


'''                 ****    Movie   ****                   '''


class GenreYear:
    @classmethod
    def get_genres(cls):
        return Genre.objects.annotate(movies_count=Count('movies'))

    @classmethod
    def get_movies(cls):
        return Movie.objects.all()

    @classmethod
    def get_years(cls):
        return cls.get_movies().values('year').order_by('-year')


class MovieListView(GenreYear, ListView):
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
        return GenreYear.get_movies().order_by('pk')


class FilterMoviesView(GenreYear, ListView):
    model = Movie
    template_name = 'mainapp/movie/filter_movies_list.html'
    context_object_name = 'movies'

    def get_queryset(self):
        queryset = GenreYear.get_movies()

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


class AboutMovieView(GenreYear, DetailView):
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


class AddMovieView(LoginRequiredMixin, CreateView):
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


class UpdateMovieView(LoginRequiredMixin, UpdateView):
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


class DeleteMovieView(LoginRequiredMixin, DeleteView):
    model = Movie
    template_name = 'mainapp/movie/delete_movie.html'
    context_object_name = 'movie'
    login_url = reverse_lazy('home')
    success_url = reverse_lazy('home')
    slug_url_kwarg = 'movie_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete movie'

        return context


'''                 ****    Actor   ****                   '''


class AboutActorView(DetailView):
    model = Actor
    template_name = 'mainapp/actor/about_actor.html'
    context_object_name = 'actor'
    slug_url_kwarg = 'actor_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'About ' + str(context['actor'].name)

        return context


class AddActorView(LoginRequiredMixin, CreateView):
    form_class = ActorForm
    template_name = 'mainapp/actor/add_actor.html'
    context_object_name = 'form'
    login_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add actor'

        return context

    def get_success_url(self):
        return reverse_lazy('about_actor', kwargs={'actor_slug': self.object.slug})


class UpdateActorView(LoginRequiredMixin, UpdateView):
    model = Actor
    form_class = ActorForm
    template_name = 'mainapp/actor/update_actor.html'
    login_url = reverse_lazy('home')
    slug_url_kwarg = 'actor_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update actor'

        return context

    def get_success_url(self):
        return reverse_lazy('about_actor', kwargs={'actor_slug': self.object.slug})


class DeleteActorView(LoginRequiredMixin, DeleteView):
    model = Actor
    template_name = 'mainapp/actor/delete_actor.html'
    context_object_name = 'actor'
    login_url = reverse_lazy('home')
    success_url = reverse_lazy('home')
    slug_url_kwarg = 'actor_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'delete actor'

        return context


'''                 ****    Director   ****                   '''


class AboutDirectorView(DetailView):
    model = Director
    template_name = 'mainapp/director/about_director.html'
    context_object_name = 'director'
    slug_url_kwarg = 'director_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'About ' + str(context['director'].name)

        return context


class AddDirectorView(LoginRequiredMixin, CreateView):
    form_class = DirectorForm
    template_name = 'mainapp/director/add_director.html'
    context_object_name = 'form'
    login_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add director'

        return context

    def get_success_url(self):
        return reverse_lazy('about_director', kwargs={'director_slug': self.object.slug})


class UpdateDirectorView(LoginRequiredMixin, UpdateView):
    model = Director
    form_class = ActorForm
    template_name = 'mainapp/director/update_director.html'
    login_url = reverse_lazy('home')
    slug_url_kwarg = 'director_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update director'

        return context

    def get_success_url(self):
        return reverse_lazy('about_director', kwargs={'director_slug': self.object.slug})


class DeleteDirectorView(LoginRequiredMixin, DeleteView):
    model = Director
    template_name = 'mainapp/director/delete_director.html'
    context_object_name = 'director'
    login_url = reverse_lazy('home')
    success_url = reverse_lazy('home')
    slug_url_kwarg = 'director_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete director'

        return context


'''                 ****    Genre   ****                   '''


class GenreListView(GenreYear, ListView):
    model = Movie
    template_name = 'mainapp/genre/show_genre.html'
    context_object_name = 'movies'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Genre ' + Genre.objects.get(slug=self.kwargs['genre_slug']).name

        return context

    def get_queryset(self):
        return Movie.objects.filter(genres__slug=self.kwargs['genre_slug']).order_by('create_time')


class AddGenreView(LoginRequiredMixin, CreateView):
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


class UpdateCommentView(LoginRequiredMixin, UpdateView):
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


class DeleteCommentView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'mainapp/comment/delete_comment.html'
    context_object_name = 'comment'
    login_url = reverse_lazy('home')
    success_url = reverse_lazy('home')
    pk_url_kwarg = 'comment_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete director'

        return context

    def get_success_url(self):
        return reverse_lazy('about_movie', kwargs={'movie_slug': self.object.movie.slug})

