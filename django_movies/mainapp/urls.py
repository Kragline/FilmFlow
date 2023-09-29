from django.urls import path
from .views import *


urlpatterns = [
    # Movie
    path('', MovieListView.as_view(), name='home'),
    path('filter/', FilterMoviesView.as_view(), name='filter'),
    path('add_movie/', AddMovieView.as_view(), name='add_movie'),
    path('movie/<slug:movie_slug>/', AboutMovieView.as_view(), name='about_movie'),
    path('movie/<slug:movie_slug>/update/', UpdateMovieView.as_view(), name='update_movie'),
    path('movie/<slug:movie_slug>/delete/', DeleteMovieView.as_view(), name='delete_movie'),

    # Actor
    path('add_actor/', AddActorView.as_view(), name='add_actor'),
    path('actor/<slug:actor_slug>/', AboutActorView.as_view(), name='about_actor'),
    path('actor/<slug:actor_slug>/update/', UpdateActorView.as_view(), name='update_actor'),
    path('actor/<slug:actor_slug>/delete/', DeleteActorView.as_view(), name='delete_actor'),

    # Director
    path('add_director/', AddDirectorView.as_view(), name='add_director'),
    path('director/<slug:director_slug>/', AboutDirectorView.as_view(), name='about_director'),
    path('director/<slug:director_slug>/update/', UpdateDirectorView.as_view(), name='update_director'),
    path('director/<slug:director_slug>/delete/', DeleteDirectorView.as_view(), name='delete_director'),

    # Genre
    path('movie/genre/<slug:genre_slug>/', GenreListView.as_view(), name='genre'),
    path('add_genre/', AddGenreView.as_view(), name='add_genre'),

    # Comment
    path('movie/<slug:movie_slug>/comment/<int:comment_id>/update/', UpdateCommentView.as_view(), name='update_comment'),
    path('movie/<slug:movie_slug>/comment/<int:comment_id>/delete/', DeleteCommentView.as_view(), name='delete_comment'),
    path('movie/<slug:movie_slug>/comment/<int:comment_id>/like/', LikeCommentView.as_view(), name='like_comment'),

    # Saga
    path('add_saga/', AddSagaView.as_view(), name='add_saga'),
]
