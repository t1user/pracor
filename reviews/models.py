from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=60)
    overallscore_score = models.PositiveIntegerField(editable=False,
                                                     default=0)
    advancement_score = models.PositiveIntegerField(editable=False,
                                                    default=0)
    worklife_score = models.PositiveIntegerField(editable=False,
                                                 default=0)
    compensation_score = models.PositiveIntegerField(editable=False,
                                                     default=0)
    environment_score = models.PositiveIntegerField(editable=False,
                                                    default=0)
    number_of_reviews = models.PositiveIntegerField(editable=False,
                                                    default=0)


class Review(models.Model):
    company = models.ForeignKey(Company,
                         verbose_name="recenzja firmy",
                         )
    date = models.DateTimeField(auto_now=True, editable=False)
    position = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    years_at_company = models.PositiveIntegerField()
    pros = models.CharField(max_length=500)
    cons = models.CharField(max_length=500)
    comment = models.TextField()
    overallscore = models.PositiveIntegerField('ocena ogólna')
    advancement = models.PositiveIntegerField('możliwości rozwoju')
    worklife = models.PositiveIntegerField('równowaga praca/życie')
    compensation = models.PositiveIntegerField('zarobki')
    environment = models.PositiveIntegerField('atmosfera w pracy')

    
class Salary(models.Model):
    company = models.ForeignKey(Company)
    position = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    years_at_company = models.PositiveIntegerField()
    years_experience = models.PositiveIntegerField()
    sex = models.CharField(max_length=1,
                           choices=[('m', 'm'), ('f', 'k')],
                           editable=False
                           )
    date = models.DateTimeField(auto_now=True, editable=False)
    status_zatrudnienia = [
        ('a', 'pełny etat - umowa na czas nieokreślony'),
        ('b', 'część etatu - umowa na czas nieokreślony'),
        ('c', 'pełny etat - umowa na czas określony'),
        ('d', 'część etatu - umowa na czas określony'),
        ('e', 'umowa zlecenie'),
        ('f', 'samozatrudnienie')
        ]
    employment_status = models.CharField(max_length=1,
                                         choices=status_zatrudnienia)
    salary = models.PositiveIntegerField()
    
