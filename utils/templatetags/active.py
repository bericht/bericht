from django.core.urlresolvers import reverse
from django import template

register = template.Library()


@register.simple_tag
def active(request, view):
    if request.path == reverse(view):
        return 'active'
    return ''
