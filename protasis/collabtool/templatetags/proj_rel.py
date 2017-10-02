from django import template

register = template.Library()


@register.inclusion_tag('proj_rel.html', takes_context=True)
def proj_rel(context):
    """ inclusion tag to show publications in project """

    return {'project': context['project'], 'rel': context['rel']}
