from django import template
import math

register = template.Library()

@register.filter
def miliseconds_to_minutes(value):
    second = value/1000
    minutes = int(second//60)
    seconds = round(second%60)

    return f"{minutes}:{seconds}"
