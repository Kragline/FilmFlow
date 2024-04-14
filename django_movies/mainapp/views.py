from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Count
from .models import Rating
from .forms import *


'''                 ****    Base Classes   ****                   '''


class SidebarData():
    NOT_EMPTY_GENRES = Genre.objects.annotate(movies_count=Count('movies')).filter(movies_count__gt=0)

    ALL_MOVIES = Movie.objects.all()
    ALL_YEARS = ALL_MOVIES.values('year').order_by('-year').distinct()
    ALL_COUNTRIES = ALL_MOVIES.values('country').order_by().distinct()
    LASTEST_PREMIERES = ALL_MOVIES.order_by('-world_premiere')[:4]
    RECENTLY_ADDED = ALL_MOVIES.order_by('-pk')[:10]


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


'''                 ****    Movie   ****                   '''


class MovieListView(SidebarData, ListView):
    model = Movie
    template_name = 'mainapp/movie/movies_list.html'
    context_object_name = 'movies'
    context_title = 'Select your favorite'
    search_mode = 'pk'
    paginate_by = 9

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.context_title
        context['title'] = 'FilmFlow - Online cinema'

        return context

    def get_queryset(self):
        queryset = SidebarData.ALL_MOVIES.order_by('id')

        if self.request.method == 'GET':
            if query := self.request.GET.get('movie-search'):
                queryset = queryset.filter(title__icontains=query)

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

    def rate_movie(self):
        rating_score = int(self.request.POST.get('rating_radio'))
        rating, created = Rating.objects.update_or_create(
            movie=self.get_object(),
            user=self.request.user, defaults={
                'score': rating_score
            })
        print(rating)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.movie = self.get_object()
                new_comment.author = request.user
                new_comment.save()

                return redirect(self.get_object())
            else:
                self.rate_movie()
                return redirect(self.get_object())
        else:
            comment_form = CommentForm()

        return reverse_lazy('about_movie', kwargs={'movie_slug': self.get_object().slug})
    
    def get_avg_rating(self, queryset):
        rating_sum = 0
        for rating in queryset:
            rating_sum += rating.score

        return round(rating_sum / len(queryset), 1)


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
            context['avg_rating'] = self.get_avg_rating(movie_ratings)

        return context


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
