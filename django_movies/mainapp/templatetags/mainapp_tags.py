from django import template


register = template.Library()


@register.simple_tag()
def get_models_movies(model):
    movies = model.movies.all()
    actor_movies = ''
    for movie in movies:
        actor_movies += movie.title + ', '

    return actor_movies.rstrip(', ')


@register.simple_tag()
def get_movie_actors(movie):
    return movie.actors.all()[:4]


@register.simple_tag()
def colored_stars_range(number):
    return range(number)


@register.simple_tag()
def other_stars_range(number):
    return range(10-number)
