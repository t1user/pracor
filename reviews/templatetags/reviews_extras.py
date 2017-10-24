from django import template

register = template.Library()

@register.filter('klass')
def klass(ob):
    return ob.__class__.__name__

@register.filter('class')
def attrs(ob):
    return ob.get('class', '')

@register.filter('thermometer')
def thermo(obj):
    dictionary = {
        1: 'empty',
        2: 'quarter',
        3: 'half',
        4: 'three-quarters',
        5: 'full',
    }

    return dictionary[obj]


@register.filter('difficulty')
def diff(obj):
    dictionary = {
        1: 'Bardzo łatwo',
        2: 'Łatwo',
        3: 'Średnia trudność',
        4: 'Trudno',
        5: 'Bardzo trudno',
    }
    return dictionary[obj]
