from django import template

register = template.Library()


@register.inclusion_tag('proj_pubs.html', takes_context=True)
def proj_publications(context):
    """ inclusion tag to show publications in project """
    return {'project': context['project']}
