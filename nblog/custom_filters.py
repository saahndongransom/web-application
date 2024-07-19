from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
@mark_safe
def responsive_images(value):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(value, 'html.parser')
    for img in soup.find_all('img'):
        img['class'] = img.get('class', []) + ['img-responsive']
    return str(soup)
