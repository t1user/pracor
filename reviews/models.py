from django.db import models
from django.urls import reverse
from django.conf import settings


class Profile(models.Model):
    SEX = [('M', 'Mężczyzna'), ('K', 'Kobieta')]

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    contributed = models.BooleanField(default=False, editable=False)
    sex = models.CharField(max_length=1, choices=SEX)
    career_start_year = models.PositiveIntegerField()    

    
class Company(models.Model):
    class Meta:
        ordering=['name']

    name = models.CharField(max_length=100, unique=True)
    headquarters_city = models.CharField(max_length=60)
    website = models.URLField(unique=True)
    overallscore = models.PositiveIntegerField(editable=False,
                                                     default=0)
    advancement = models.PositiveIntegerField(editable=False,
                                                    default=0)
    worklife = models.PositiveIntegerField(editable=False,
                                                 default=0)
    compensation = models.PositiveIntegerField(editable=False,
                                                     default=0)
    environment = models.PositiveIntegerField(editable=False,
                                                    default=0)
    number_of_reviews = models.PositiveIntegerField(editable=False,
                                                    default=0)


    def get_reviews(self):
        return  Review.objects.filter(company=self.pk)

    def get_salaries(self):
        return  Salary.objects.filter(company=self.pk)

    def get_interviews(self):
        return Interview.objects.filter(company=self.pk)

    def get_scores(self):
        if self.number_of_reviews != 0:
            overallscore = round(self.overallscore/self.number_of_reviews, 1)
            advancement = round(self.advancement/self.number_of_reviews, 1)
            worklife = round(self.worklife/self.number_of_reviews, 1)
            compensation = round(self.compensation/self.number_of_reviews, 1)
            environment = round(self.environment/self.number_of_reviews, 1)
            return {'overallscore': overallscore,
                    'advancement': advancement,
                    'worklife': worklife,
                    'compensation': compensation,
                    'environment': environment,
            }
        

    def update_scores(self):
        """
        Method recalculates all scores to make them compliant with existing reviews.
        """
        reviews = self.get_reviews()
        self.overallscore = 0
        self.advancement = 0
        self.worklife = 0
        self.compensation = 0
        self.environment = 0
        self.number_of_reviews = reviews.count()
        for review in reviews:
            self.overallscore += review.overallscore
            self.advancement += review.advancement
            self.worklife += review.worklife
            self.compensation += review.compensation
            self.environment += review.environment
        self.save()
            
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('company_page',
                       kwargs={'pk': self.pk})

class Position(models.Model):
    STATUS_ZATRUDNIENIA = [
        ('A', 'Pełen etat'),
        ('B', 'Część etatu'),
        ('C', 'Zlecenie'),
        ('D', 'Samozazatrudnienie'),
        ('E', 'Inne'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    years_at_company = models.PositiveIntegerField()
    employment_status = models.CharField(max_length=1,
                                         choices=STATUS_ZATRUDNIENIA,
                                         default='A')
    

class Review(Position):
    #company = models.ForeignKey(Company, on_delete=models.CASCADE)
    #position = models.ForeignKey(Position, on_delete=models.CASCADE)
    #position = models.OneToOneField(Position, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True, editable=False)
    title = models.CharField(max_length=100)
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


class Salary(Position):
    PERIOD = [
        ('M', 'miesięcznie'),
        ('R', 'rocznie'),
        ('G', 'na godzinę'),
    ]
    GROSS_NET = [
        ('G', 'brutto'),
        ('N', 'netto'),
    ]
    
    #company = models.ForeignKey(Company, on_delete=models.CASCADE)
    #position = models.ForeignKey(Position, on_delete=models.CASCADE, blank=True)
    #position = models.OneToOneField(Position, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True, editable=False)

    currency = models.CharField('waluta',
                                max_length=3, default='PLN')

    salary_input = models.PositiveIntegerField('pensja')
    period = models.CharField('za okres',
                              max_length=1, default='M', choices=PERIOD)
    gross_net = models.CharField('', max_length=1, default='G', choices=GROSS_NET)

    bonus_input = models.PositiveIntegerField('premia', default=0)
    bonus_period = models.CharField('',
                                    max_length=1, default='M', choices=PERIOD)
    bonus_gross_net = models.CharField('',
                                       max_length=1, default='G', choices=GROSS_NET)

    base_monthly = models.PositiveIntegerField(blank=True,
                                              default=0, editable=False)
    base_annual = models.PositiveIntegerField(blank=True,
                                              default=0, editable=False)

    total_monthly = models.PositiveIntegerField(blank=True,
                                               default=0, editable=False)
    total_annual = models.PositiveIntegerField(blank=True,
                                               default=0, editable=False)
    
    
    def get_absolute_url(self):
        return reverse('company_page',
                       kwargs={'pk': self.company.id})

    def __str__(self):
        return 'id_' + str(self.id)

class Interview(models.Model):
    HOW_GOT = [
        ('A', 'Ogłoszenie'),
        ('B', 'Kontakty profesjonalne'),
        ('C', 'Head-hunter'),
        ('D', 'Znajomi-rodzina'),
        ('E', 'Sex z decydentem'),
        ('F', 'Inne'),
    ]
    DIFFICULTY = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True, editable=False)
    position = models.CharField('stanowisko',
                                max_length=100, blank=True)
    department = models.CharField('departament',
                                  max_length=100, blank=True)
    how_got = models.CharField('droga do interview',
                               max_length=1, choices=HOW_GOT, default=None)
    difficulty = models.PositiveIntegerField('trudność',
                                             choices=DIFFICULTY)
    got_offer = models.BooleanField('czy dostał ofertę',
                                    blank=True)
    questions = models.TextField('pytania')
    impressions = models.CharField('wrażenia',
                                   max_length=100, blank=True)

    def get_absolute_url(self):
        return reverse('company_page',
                       kwargs={'pk': self.company.id})

    def __str__(self):
        return 'id_' + str(self.id)
