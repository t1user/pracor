from django import template
from reviews.models import Review, Salary

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
    compensation, etc. Review fields.
    """
    return Review._meta.get_field(name).verbose_name.capitalize()


@register.filter('file')
def file_name(model):
    """
    Return correct file to render Reviews, Salaries or Interviews.
    """
    depluralize = {
        'reviews': 'review',
        'salaries': 'salary',
        'interviews': 'interview',
    }

    if model in ['reviews', 'salaries', 'interviews']:
        model = depluralize[model]

    dictionary = {
        'review': 'reviews/_review_item.html',
        'salary': 'reviews/_salary_item.html',
        'interview': 'reviews/_interview_item.html',
    }

    return dictionary[model]


@register.filter('translate')
def translate_item(item):
    """
    Translate model name to required Polish url component name.
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
        obj = Salary.objects.filter(period=item)[0]
    except:
        return
    return obj.get_period_display()
    # return Salary.get_period_display(item)


@register.filter('gross_net')
def translate_gross_net(item):
    try:
        obj = Salary.objects.filter(gross_net=item)[0]
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


@register.filter('make_percent')
def make_percent(distance, range):
    if range != 0:
        return str((distance / range) * 100 + 5
                   ) + '%'
    return '55%'

@register.filter('width')
def make_per(obj):
    distance=(obj['salary_max'] - obj['salary_avg'])
    range=(obj['salary_max'] - obj['salary_min'])
    if range != 0:
        return str((distance / range) * 100 + 5) + '%'
    return '55%'


