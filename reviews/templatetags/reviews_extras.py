from django import template
from reviews.models import Review, Salary
from django.contrib.postgres.aggregates.general import StringAgg

register = template.Library()


@register.filter('klass')
def klass(ob):
    return ob.__class__.__name__


@register.filter('class')
def attrs(ob):
    """
    CURRENTLY NOT IN USE
    """
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
    """
    Translate numeric difficulty assesment from Interview model into associated text
    string in templates.
    """
    dictionary = {
        1: 'Bardzo łatwa rozmowa',
        2: 'Łatwa rozmowa',
        3: 'Średnio-trudna rozmowa',
        4: 'Trudna rozmowa',
        5: 'Bardzo trudna rozmowa',
    }
    return dictionary[obj]


@register.filter('stars')
def star_generator(rating):
    """
    Take a rating score and return iterators (range(...) objects) 
    for number of full and empty star icons and 1 or 0 for half-star.
    Rating is a value representing rating that needs to be converted into
    stars widget.
    """
    if rating == '':
        return None

    truncated = int(rating)
    half = rating - truncated
    if 0.25 <= half < 0.75:
        half = 1
    else:
        half = 0
    if rating - truncated >= 0.75:
        truncated += 1
    # full and blank are iterators to allow for looping in templates
    # half is always either one or zero
    full = range(truncated)
    blank = range(5 - truncated - half)
    return {
        "full": full,
        "half": half,
        "blank": blank,
    }



@register.filter('rating_name')
def rating_name(name):
    """
    Convert variable name into displayable field name. Used for overallscore, worklife, 
    compensation, etc. Review fields in _rating_item.html
    """
    return Review._meta.get_field(name).verbose_name.capitalize()


@register.filter('file')
def file_name(model):
    """
    Return correct file to render Reviews, Salaries or Interviews.
    """
    return 'reviews/_{}_item.html'.format(model)

@register.filter('file_header')
def file_header(model):
    """
    Return correct file to render headers for Reviews, Salaries or Interviews.
    """
    return 'reviews/_{}_header.html'.format(model)
    
@register.filter('translate')
def translate_item(item):
    """
    Translate model name to required Polish url segment name.
    """
    dictionary = {
        'review': 'opinie',
        'salary': 'zarobki',
        'interview': 'rozmowy',
    }
    return dictionary[item]


@register.filter('period')
def translate_period(item):
    """
    Rosolve salary.period database choices into display values.
    """
    try:
        obj = Salary.objects.filter(period=item).last()
        return obj.get_period_display()
    except AttributeError:
        return ''

    
@register.filter('contract')
def translate_period(item):
    """
    Rosolve salary.contract_type database choices into display values.
    """
    try:
        obj = Salary.objects.filter(contract_type=item).last()
        return obj.get_contract_type_display()
    except AttributeError:
        return ''
    
    
@register.filter('bonus_period')
def translate_bonus_period(items):
    output = []
    for item in items:
        if item is None:
            continue
        try:
            obj = Salary.objects.filter(bonus_period=item).last()
            output.append(obj.get_bonus_period_display())
        except AttributeError:
            output += ''
    return ', '.join(output)

@register.filter('gross_net')
def translate_gross_net(item):
    try:
        obj = Salary.objects.filter(gross_net=item).last()
    except:
        return
    return obj.get_gross_net_display()


@register.filter('item_name_singular')
def item_name(item):
    dictionary = {'review': 'opinię',
                  'salary': 'zarobki',
                  'interview': 'rozmowę'}
    return dictionary[item]


@register.filter('item_list_title')
def item_list_tittle(item):
    dictionary = {
        'review': 'Opinie o firmie:',
        'salary': 'Zarobki w firmie:',
        'interview': 'Rozmowy kwalifikacyjne w firmie:',
    }
    return dictionary[item]


@register.filter('width')
def make_percent(obj, item):
    distance=(obj[item+'_max'] - obj[item+'_avg'])
    range=(obj[item+'_max'] - obj[item+'_min'])
    if range != 0:
        return str((distance / range) * 100 + 5) + '%'
    return '55%'


@register.filter('min_slider')
def min_slider(obj, item):
    return obj[item+'_min']

@register.filter('max_slider')
def max_slider(obj, item):
    return obj[item+'_max']

@register.filter('count_slider')
def count_slider(obj, item):
    return obj[item+'_count']


@register.filter('benefits')
def benefits(obj_list):
    """
    Return string of all Benefit names related to the Salaries, 
    whose id's are passed in obj_list.
    """
    return(Salary.objects.filter(
        id__in=obj_list).aggregate(list=StringAgg(
            'benefits__name', distinct=True, delimiter = ', '))['list'])

