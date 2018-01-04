from django.db import models
from django.db.models import Avg, Max, Min, Count
from django.contrib.postgres.aggregates import StringAgg


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
        field = models.FloatField()
        return self.selected(**kwargs).values(
            'position__position',
            'position__location',
            'position__department',
            'currency',
            'period',
        ).annotate(
            salary_min = Min('salary_input_gross'),
            salary_avg = Avg('salary_input_gross', output_field=models.IntegerField()),
            salary_max = Max('salary_input_gross'),
            salary_count = Count('salary_input_gross'),
            bonus_min = Min('bonus_anual'),
            bonus_avg = Avg('bonus_anual', output_field=models.IntegerField()),
            bonus_max = Max('bonus_anual'),
            bonus_count = Count('bonus_anual'),
            bonus_periods = StringAgg('bonus_period', ',', distinct=True),
        )

