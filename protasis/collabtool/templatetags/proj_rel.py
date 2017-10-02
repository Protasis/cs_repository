from django import template

register = template.Library()


@register.inclusion_tag('proj_rel.html', takes_context=True)
def proj_rel(context):
    """ inclusion tag to show publications in project """

    cl = context['cl']
    return {'p': context[cl], 'rel': context['rel']}

@register.filter
def get_class(obj):
    return obj.__class__.__name__
