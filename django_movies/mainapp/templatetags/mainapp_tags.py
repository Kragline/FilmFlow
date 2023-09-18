from django import template


register = template.Library()


@register.simple_tag()
def get_movie_actors(movie):
    data = movie.actors.all()

    if len(data) >= 4:
        return data[:4]
    elif len(data) == 2:
        return data[:2]

    return data


@register.simple_tag()
def get_actors_or_directors_movies(model):
    data = model.movies.all()

    if len(data) >= 3:
        return data[:3]
    elif len(data) == 2:
        return data[:2]

    return data


@register.simple_tag()
def colored_stars_range(number):
    return range(number)


@register.simple_tag()
def other_stars_range(number):
    return range(10-number)
