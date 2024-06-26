from django.urls import path
from .views import *


# !!! WARNING !!! urls without slugs must be always higher than those without slugs

urlpatterns = [
    # Movie
    path('', MovieListView.as_view(), name='home'),
    path('filter/', MovieListView.as_view(), name='filter'),
    path('movie/add/', AddMovieView.as_view(), name='add_movie'),
    path('movie/rate/', RateMovieView.as_view(), name='rate_movie'),
    path('movie/<slug:movie_slug>/', AboutMovieView.as_view(), name='about_movie'),
    path('movie/<slug:movie_slug>/update/', UpdateMovieView.as_view(), name='update_movie'),
    path('movie/<slug:movie_slug>/delete/', DeleteMovieView.as_view(), name='delete_movie'),

    # Actor
    path('actor/add/', AddActorView.as_view(), name='add_actor'),
    path('actor/<slug:actor_slug>/', AboutActorView.as_view(), name='about_actor'),
    path('actor/<slug:actor_slug>/update/', UpdateActorView.as_view(), name='update_actor'),
    path('actor/<slug:actor_slug>/delete/', DeleteActorView.as_view(), name='delete_actor'),

    # Director
    path('director/add/', AddDirectorView.as_view(), name='add_director'),
    path('director/<slug:director_slug>/', AboutDirectorView.as_view(), name='about_director'),
    path('director/<slug:director_slug>/update/', UpdateDirectorView.as_view(), name='update_director'),
    path('director/<slug:director_slug>/delete/', DeleteDirectorView.as_view(), name='delete_director'),

    # Genre
    path('movie/genre/add/', AddGenreView.as_view(), name='add_genre'),
    path('movie/genre/<slug:genre_slug>/', GenreListView.as_view(), name='genre'),

    # Comment
    path('comment/add/', AddCommentView.as_view(), name='add_comment'),
    path('comment/like/', LikeCommentView.as_view(), name='like_comment'),
    path('comment/<slug:movie_slug>/<int:comment_id>/update/', UpdateCommentView.as_view(), name='update_comment'),
    path('comment/<slug:movie_slug>/<int:comment_id>/delete/', DeleteCommentView.as_view(), name='delete_comment'),

    # Other
    path('about-us/', AboutUsView.as_view(), name='about'),
    path('troubleshoot/', TroubleshootView.as_view(), name='troubleshoot'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
]
