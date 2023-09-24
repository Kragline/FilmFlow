from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

import datetime


class Person(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        abstract = True


class Actor(Person):
    photo = models.ImageField(upload_to='actor_photos')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('about_actor', kwargs={'actor_slug': self.slug})

    def get_absolute_url_for_update(self):
        return reverse('update_actor', kwargs={'actor_slug': self.slug})

    def get_absolute_url_for_delete(self):
        return reverse('delete_actor', kwargs={'actor_slug': self.slug})

    class Meta:
        verbose_name = 'Actor'
        verbose_name_plural = 'Actors'


class Director(Person):
    photo = models.ImageField(upload_to='director_photos')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('about_director', kwargs={'director_slug': self.slug})

    def get_absolute_url_for_update(self):
        return reverse('update_director', kwargs={'director_slug': self.slug})

    def get_absolute_url_for_delete(self):
        return reverse('delete_director', kwargs={'director_slug': self.slug})

    class Meta:
        verbose_name = 'Director'
        verbose_name_plural = 'Directors'


class Genre(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('genre', kwargs={'genre_slug': self.slug})

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Movie(models.Model):
    title = models.CharField(max_length=150)
    tagline = models.CharField(blank=True, max_length=150)
    about = models.TextField(blank=True)
    year = models.PositiveSmallIntegerField()
    country = models.CharField(max_length=150)
    world_premiere = models.DateField(default=datetime.date.today)
    poster = models.ImageField(upload_to='movie_posters')
    video = models.FileField(upload_to='movie_trailers', blank=True)
    actors = models.ManyToManyField(Actor, related_name='movies')
    directors = models.ManyToManyField(Director, related_name='movies')
    genres = models.ManyToManyField(Genre, related_name='movies')
    rating = models.PositiveSmallIntegerField(default=1, blank=True)
    budget = models.PositiveIntegerField(default=0, help_text='Budget in US dollars')
    fees = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('about_movie', kwargs={'movie_slug': self.slug})

    def get_absolute_url_for_update(self):
        return reverse('update_movie', kwargs={'movie_slug': self.slug})

    def get_absolute_url_for_delete(self):
        return reverse('delete_movie', kwargs={'movie_slug': self.slug})

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('about_comment', kwargs={'comment_id': self.pk, 'movie_slug': self.movie.slug})

    def get_absolute_url_for_update(self):
        return reverse('update_comment', kwargs={'comment_id': self.pk, 'movie_slug': self.movie.slug})

    def get_absolute_url_for_delete(self):
        return reverse('delete_comment', kwargs={'comment_id': self.pk, 'movie_slug': self.movie.slug})
