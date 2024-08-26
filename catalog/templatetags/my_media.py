from django import template

register = template.Library()


@register.filter(name='media_url')
def media_url(value):
    return f'/media/{value}'
