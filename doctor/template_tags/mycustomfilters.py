from django import template
register = template.Library()

@register.filter(name = 'splitByHash')
def splitByHash(value):
    d = value.split('#')
    d.reverse()
    return d[0]

@register.filter(name = 'splitByAdtherate')
def splitByAdtherate(value):
    d = value.split('@')
    d.reverse()
    return d[0]
