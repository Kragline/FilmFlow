from django import template


register = template.Library()


@register.simple_tag()
def colored_stars_range(number):
    return range(number)


@register.filter(name='format_money')
def format_money(money):
    money = str(money)
    formatted_money = f'{money[:-6]} million $' if len(money) <= 9 else f'{money[:-9]} billion $'

    return formatted_money
