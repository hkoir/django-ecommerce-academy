from django import template

register = template.Library()

@register.filter(name='currency')
def currency(number):
    return "BDT "+str(number)



@register.filter(name='multiply')
def multiply(number , number1):
    return number * number1


@register.filter
def display_stars(rating):
    full_stars = int(rating)
    half_stars = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_stars

    return '★' * full_stars + '½' * half_stars + '☆' * empty_stars
