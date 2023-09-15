from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Count

from .forms import *
from .utils import *

'''                 ****    Movie   ****                   '''


class MovieListView(DataMixin, ListView):
    model = Movie
    template_name = 'mainapp/movie/movies_list.html'
    context_object_name = 'movies'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Movies')

        return dict(list(context.items()) + list(mixin_context.items()))

    def get_queryset(self):
        query = self.request.GET.get('movie-search')
        search_mode = self.request.GET.get('search-mode')
        queryset = Movie.objects.order_by('create_time')

        if self.request.method == 'GET':
            if query is not None:
                queryset = queryset.filter(title__contains=query)
            if search_mode:
                queryset = queryset.order_by(search_mode)

        return queryset


class AboutMovieView(DataMixin, DetailView):
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
        mixin_context = self.get_user_context(form=CommentForm(), comments=self.object.comments.order_by('-create_time'))

        return dict(list(context.items()) + list(mixin_context.items()))


class AddMovieView(LoginRequiredMixin, DataMixin, CreateView):
    form_class = MovieForm
    template_name = 'mainapp/movie/add_movie.html'
    context_object_name = 'form'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Add movie')

        return dict(list(context.items()) + list(mixin_context.items()))


class UpdateMovieView(LoginRequiredMixin, DataMixin, UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = 'mainapp/movie/update_movie.html'
    login_url = reverse_lazy('home')
    slug_url_kwarg = 'movie_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Update movie')

        return dict(list(context.items()) + list(mixin_context.items()))

    def get_success_url(self):
        return reverse_lazy('about_movie', kwargs={'movie_slug': self.object.slug})


class DeleteMovieView(LoginRequiredMixin, DataMixin, DeleteView):
    model = Movie
    template_name = 'mainapp/movie/delete_movie.html'
    context_object_name = 'movie'
    login_url = reverse_lazy('home')
    success_url = reverse_lazy('home')
    slug_url_kwarg = 'movie_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Delete movie')

        return dict(list(context.items()) + list(mixin_context.items()))


'''                 ****    Actor   ****                   '''


class ActorsListView(DataMixin, ListView):
    model = Actor
    template_name = 'mainapp/actor/actors_list.html'
    context_object_name = 'actors'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Actors')

        return dict(list(context.items()) + list(mixin_context.items()))

    def get_queryset(self):
        query = self.request.GET.get('actor-search')
        search_mode = self.request.GET.get('search-mode')
        queryset = Actor.objects.order_by('create_time')

        if self.request.method == 'GET':
            if query is not None:
                queryset = queryset.filter(name__contains=query)
            if search_mode:
                queryset = queryset.order_by(search_mode)

        return queryset


class AboutActorView(DataMixin, DetailView):
    model = Actor
    template_name = 'mainapp/actor/about_actor.html'
    context_object_name = 'actor'
    slug_url_kwarg = 'actor_slug'  # changing default slug name to what we need

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='About ' + str(context['actor'].name))

        return dict(list(context.items()) + list(mixin_context.items()))


class AddActorView(LoginRequiredMixin, DataMixin, CreateView):
    form_class = ActorForm
    template_name = 'mainapp/actor/add_actor.html'
    context_object_name = 'form'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Add actor')

        return dict(list(context.items()) + list(mixin_context.items()))


class UpdateActorView(LoginRequiredMixin, DataMixin, UpdateView):
    model = Actor
    form_class = ActorForm
    template_name = 'mainapp/actor/update_actor.html'
    login_url = reverse_lazy('home')
    slug_url_kwarg = 'actor_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Update actor')

        return dict(list(context.items()) + list(mixin_context.items()))

    def get_success_url(self):
        return reverse_lazy('about_actor', kwargs={'actor_slug': self.object.slug})


class DeleteActorView(LoginRequiredMixin, DataMixin, DeleteView):
    model = Actor
    template_name = 'mainapp/actor/delete_actor.html'
    context_object_name = 'actor'
    login_url = reverse_lazy('home')
    success_url = reverse_lazy('home')
    slug_url_kwarg = 'actor_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Delete actor')

        return dict(list(context.items()) + list(mixin_context.items()))


'''                 ****    Actor   ****                   '''


class DirectorsListView(DataMixin, ListView):
    model = Director
    template_name = 'mainapp/director/directors_list.html'
    context_object_name = 'directors'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Directors')

        return dict(list(context.items()) + list(mixin_context.items()))

    def get_queryset(self):
        query = self.request.GET.get('director-search')
        search_mode = self.request.GET.get('search-mode')
        queryset = Director.objects.order_by('create_time')

        if self.request.method == 'GET':
            if query is not None:
                queryset = queryset.filter(name__contains=query)
            if search_mode:
                queryset = queryset.order_by(search_mode)

        return queryset


class AboutDirectorView(DataMixin, DetailView):
    model = Director
    template_name = 'mainapp/director/about_director.html'
    context_object_name = 'director'
    slug_url_kwarg = 'director_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='About ' + str(context['director'].name))

        return dict(list(context.items()) + list(mixin_context.items()))


class AddDirectorView(LoginRequiredMixin, DataMixin, CreateView):
    form_class = DirectorForm
    template_name = 'mainapp/director/add_director.html'
    context_object_name = 'form'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Add director')

        return dict(list(context.items()) + list(mixin_context.items()))


class UpdateDirectorView(LoginRequiredMixin, DataMixin, UpdateView):
    model = Director
    form_class = ActorForm
    template_name = 'mainapp/director/update_director.html'
    login_url = reverse_lazy('home')
    slug_url_kwarg = 'director_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Update director')

        return dict(list(context.items()) + list(mixin_context.items()))

    def get_success_url(self):
        return reverse_lazy('about_director', kwargs={'director_slug': self.object.slug})


class DeleteDirectorView(LoginRequiredMixin, DataMixin, DeleteView):
    model = Director
    template_name = 'mainapp/director/delete_director.html'
    context_object_name = 'director'
    login_url = reverse_lazy('home')
    success_url = reverse_lazy('home')
    slug_url_kwarg = 'director_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Delete director')

        return dict(list(context.items()) + list(mixin_context.items()))


'''                 ****    Genre   ****                   '''


class GenreListView(DataMixin, ListView):
    model = Movie
    template_name = 'mainapp/comment/comment.html'
    context_object_name = 'movies'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Genre ' + context['movies'][0].category.name)

        return dict(list(context.items()) + list(mixin_context.items()))

    def get_queryset(self):
        return Movie.objects.filter(category__slug=self.kwargs['genre_slug']).order_by('create_time')


class AddGenreView(LoginRequiredMixin, DataMixin, CreateView):
    form_class = GenreForm
    template_name = 'mainapp/comment/add_genre.html'
    context_object_name = 'form'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Add comment')

        return dict(list(context.items()) + list(mixin_context.items()))


'''                 ****    Comment   ****                   '''


class UpdateCommentView(LoginRequiredMixin, DataMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'mainapp/comment/update_comment.html'
    context_object_name = 'form'
    login_url = reverse_lazy('home')
    pk_url_kwarg = 'comment_id'
    slug_url_kwarg = 'movie_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Update comment')

        return dict(list(context.items()) + list(mixin_context.items()))

    def get_success_url(self):
        return reverse_lazy('about_movie', kwargs={'movie_slug': self.object.movie.slug})


class DeleteCommentView(LoginRequiredMixin, DataMixin, DeleteView):
    model = Comment
    template_name = 'mainapp/comment/delete_comment.html'
    context_object_name = 'comment'
    login_url = reverse_lazy('home')
    success_url = reverse_lazy('home')
    pk_url_kwarg = 'comment_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Delete comment')

        return dict(list(context.items()) + list(mixin_context.items()))

    def get_success_url(self):
        return reverse_lazy('about_movie', kwargs={'movie_slug': self.object.movie.slug})

