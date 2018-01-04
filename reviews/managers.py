from django.db import models
from django.db.models import Avg, Max, Min, Count


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
            'gross_net',
        ).annotate(
            salary_min = Min('salary_input'),
            salary_avg = Avg('salary_input', output_field=models.IntegerField()),
            salary_max = Max('salary_input'),
            salary_count = Count('salary_input'),
        )

