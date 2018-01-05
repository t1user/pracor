from django.db import models
from django.db.models import Avg, Max, Min, Count, Aggregate


class ArrayAgg(Aggregate):
    """
    Class copied from Django2.0 to provide 'distinct' functionality.
    """
    function = 'ARRAY_AGG'
    template = '%(function)s(%(distinct)s%(expressions)s)'

    def __init__(self, expression, distinct=False, **extra):
        super().__init__(expression, distinct='DISTINCT ' if distinct else '', **extra)

    def convert_value(self, value, expression, connection, *args):
        if not value:
            return []
        return value


class SelectedManager(models.Manager):
    """
    Modify standard manager to exclude items that have been 'censored'
    by moderators.
    """
    use_for_related_fields = True

    def selected(self, **kwargs):
        return self.filter(**kwargs).exclude(approved=False)

    
class SalaryManager(SelectedManager):
    """
    Group salary input data into presentable items.
    """
    use_for_related_fields = True

    def groups(self, **kwargs):
        return self.selected(**kwargs).values(
            'position__position',
            'position__location',
            'position__department',
            'currency',
            'period',
        ).annotate(
            salary_min = Min('salary_gross_input_period'),
            salary_avg = Avg('salary_gross_input_period', output_field=models.IntegerField()),
            salary_max = Max('salary_gross_input_period'),
            salary_count = Count('salary_gross_input_period'),
            bonus_min = Min('bonus_gross_input_period'),
            bonus_avg = Avg('bonus_gross_input_period', output_field=models.IntegerField()),
            bonus_max = Max('bonus_gross_input_period'),
            bonus_count = Count('bonus_gross_input_period'),
            bonus_annual_min = Min('bonus_gross_annual'),
            bonus_annual_avg = Avg('bonus_gross_annual'),
            bonus_annual_max = Max('bonus_gross_annual'),
            bonus_annual_count = Count('bonus_gross_annual'),
            #distinct=True available only in Django2.0, that's why ArrayAgg is overriden
            bonus_periods = ArrayAgg('bonus_period', distinct=True), 
        )

