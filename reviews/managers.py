from django.contrib.postgres.aggregates import ArrayAgg
from django.db import models
from django.db.models import Avg, Count, Max, Min


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
        """
        This is what is presented for Company.salaries.

        Groups lack benefits - many to many field
        (they are fetched separately in a template filter),
        because adding this annotation screws up Count to include
        the number of m2m fields in salary_count.
        """
        return (
            self.selected(**kwargs)
            .values(
                "position__position",
                "position__location",
                "position__department",
                "position__employment_status",
                "contract_type",
                "currency",
                "period",
            )
            .annotate(
                salary_min=Min("salary_gross_input_period"),
                salary_avg=Avg(
                    "salary_gross_input_period", output_field=models.IntegerField()
                ),
                salary_max=Max("salary_gross_input_period"),
                salary_count=Count("salary_gross_input_period"),
                bonus_min=Min("bonus_gross_input_period"),
                bonus_avg=Avg(
                    "bonus_gross_input_period", output_field=models.IntegerField()
                ),
                bonus_max=Max("bonus_gross_input_period"),
                bonus_count=Count("bonus_gross_input_period"),
                bonus_annual_min=Min("bonus_gross_annual"),
                bonus_annual_avg=Avg(
                    "bonus_gross_annual", output_field=models.IntegerField()
                ),
                bonus_annual_max=Max("bonus_gross_annual"),
                bonus_annual_count=Count("bonus_gross_annual"),
                bonus_periods=ArrayAgg("bonus_period", distinct=True),
                salary_object_list=ArrayAgg("id", distinct=True),
            )
        )

    def sums(self, **kwargs):
        """
        Return average, min and max of all monthly salaries in the company.
        """
        return self.selected(**kwargs).aggregate(
            sum_avg=Avg("salary_gross_annual", output=models.IntegerField()) / 12,
            sum_min=Min("salary_gross_annual", output=models.IntegerField()) / 12,
            sum_max=Max("salary_gross_annual", output=models.IntegerField()) / 12,
            sum_count=Count("salary_input"),
        )
