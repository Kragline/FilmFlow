from django import template


register = template.Library()


@register.simple_tag()
def colored_stars_range(number):
    return range(number)


@register.filter(name='format_money')
def format_money(value):
    return f'{ value / 1000000 } million $'
