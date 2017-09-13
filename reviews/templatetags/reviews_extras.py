from django import template

register = template.Library()

@register.filter('klass')
def klass(ob):
    return ob.__class__.__name__

@register.filter('class')
def attrs(ob):
    return ob.get('class', '')
