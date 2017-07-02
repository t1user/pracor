from django.db import models
from django.urls import reverse


class Company(models.Model):
    class Meta:
        ordering=['name']
        
    name = models.CharField(max_length=100, unique=True)
    headquarters_city = models.CharField(max_length=60)
    website = models.URLField(unique=True)
    overallscore_total = models.PositiveIntegerField(editable=False,
                                                     default=0)
    advancement_total = models.PositiveIntegerField(editable=False,
                                                    default=0)
    worklife_total = models.PositiveIntegerField(editable=False,
                                                 default=0)
    compensation_total = models.PositiveIntegerField(editable=False,
                                                     default=0)
    environment_total = models.PositiveIntegerField(editable=False,
                                                    default=0)
    number_of_reviews = models.PositiveIntegerField(editable=False,
                                                    default=0)
    

    def get_scores(self):
        if self.number_of_reviews != 0:
            overallscore = round(self.overallscore_total/self.number_of_reviews, 1)
            advancement = round(self.advancement_total/self.number_of_reviews, 1)
            worklife = round(self.worklife_total/self.number_of_reviews, 1)
            compensation = round(self.compensation_total/self.number_of_reviews, 1)
            environment = round(self.environment_total/self.number_of_reviews, 1)
            return {'overallscore': overallscore,
                    'advancement': advancement,
                    'worklife': worklife,
                    'compensation': compensation,
                    'environment': environment,
            }
        
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('company_page',
                       kwargs={'pk': self.pk})


class Review(models.Model):
    company = models.ForeignKey(Company)
    date = models.DateTimeField(auto_now=True, editable=False)
    position = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    years_at_company = models.PositiveIntegerField()
    pros = models.CharField(max_length=500)
    cons = models.CharField(max_length=500)
    comment = models.TextField()

    RATINGS = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    overallscore = models.PositiveIntegerField('ocena ogólna',
                                               choices=RATINGS, default=None)
    advancement = models.PositiveIntegerField('możliwości rozwoju',
                                              choices=RATINGS, default=None)
    worklife = models.PositiveIntegerField('równowaga praca-życie',
                                           choices=RATINGS, default=None)
    compensation = models.PositiveIntegerField('zarobki',
                                               choices=RATINGS, default=None)
    environment = models.PositiveIntegerField('atmosfera w pracy',
                                              choices=RATINGS, default=None)

    def get_absolute_url(self):
        return reverse('company_page',
                       kwargs={'pk': self.company.id})
    
    def __str__(self):
        return 'id_' + str(self.id)


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
        ('a', 'Pełen etat'),
        ('b', 'Część etatu'),
        ('c', 'Zlecenie'),
        ('d', 'Samozazatrudnienie'),
        ('e', 'Inne'),
    ]
    employment_status = models.CharField(max_length=1,
                                         choices=status_zatrudnienia,
                                         default='a')
    salary = models.PositiveIntegerField()

    def get_absolute_url(self):
        return reverse('company_page',
                       kwargs={'pk': self.company.id})

    def __str__(self):
        return 'id_' + str(self.id)
