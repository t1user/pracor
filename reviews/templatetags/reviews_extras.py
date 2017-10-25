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
        1: 'Bardzo łatwa rozmowa',
        2: 'Łatwa rozmowa',
        3: 'Średnio-trudna rozmowa',
        4: 'Trudna rozmowa',
        5: 'Bardzo trudna rozmowa',
    }
    return dictionary[obj]
