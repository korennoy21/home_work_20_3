from django import template

register = template.Library()


@register.filter(name='my_media')
def my_media(data):
    if data:
        return f'/media/{data}'
    return '#'