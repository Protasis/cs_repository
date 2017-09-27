from django import template

register = template.Library()


@register.simple_tag(name='projectlink')
def proj_link(p, content_type):
    return 0
