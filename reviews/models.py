import datetime

from django.conf import settings
from django.db import models
from django.db.models import Avg
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


class ApprovableModel(models.Model):
    """
    Abstract model providing features for entry approval in the admin module.
    """
    #approved set to False prevents the record from being displayed
    approved = models.NullBooleanField('Zatwierdzone', default=None, null=True, blank=True)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Zatwierdzający',
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True, editable=False)
    reviewed_date = models.DateField('Data przeglądu', null=True, blank=True)
    
    class Meta:
        abstract = True

        
class Company(ApprovableModel):
        
    EMPLOYMENT = [('A', '<100'), ('B', '101-500'), ('C', '501-1000'),
                  ('D', '1001-5000'), ('E', '5001-10000'), ('F', '>10000')]

    #only three values are required - to make company creation easy for users
    name = models.CharField('nazwa', max_length=200, unique=True)
    headquarters_city = models.CharField('siedziba centrali', max_length=60)
    website = models.URLField('strona www', unique=True)

    #other fields are optional, to be filled-in by admins (rather than users)
    date = models.DateField('data dodania do bazy', auto_now_add=True, editable=False)
    region = models.CharField('województwo', max_length=40, blank=True, null=True)
    country = models.CharField('kraj', max_length=40, default='Polska')
    employment = models.CharField('zatrudnienie', max_length=1,
                                  choices=EMPLOYMENT, blank=True, null=True)
    public = models.NullBooleanField('notowane', blank=True, null=True)
    ownership = models.TextField('właściciele', blank=True, null=True)
    sectors = models.TextField('sektory', blank=True, null=True)
    isin = models.CharField('ISIN', max_length=30, blank=True, null=True)

    slug = models.SlugField(null=True, max_length=200, editable=False)

    class Meta:
        verbose_name = "Firma"
        verbose_name_plural = "Firmy"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))
        #get rid of '-sa', '-sp-z-oo' and '-sp-z-oo-sp-k' etc. endings
        endings = ['-sa',
                   '-sp-z-oo',
                   '-sp-z-oo-sp-k',
                   '-sp-j',
                   '-sp-j-sp-j',
                   '-sp-k',
                   '-sp-j-sp-j',
                   '-sp-z-oo-ska',
                   '-sp-z-oo-sp-j',
                   ]
        for e in endings:
            if self.slug.endswith(e):
                self.slug = self.slug.replace(e, '')
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('company_page',
                       kwargs={'pk': self.pk, 'slug': self.slug})
    @property
    def reviews(self):
        return Review.objects.selected(company=self.pk)
        #return Review.objects.filter(company=self.pk).exclude(approved=False)

    @property
    def salaries(self):
        return Salary.objects.filter(company=self.pk).exclude(approved=False)

    @property
    def interviews(self):
        return Interview.objects.filter(company=self.pk).exclude(approved=False)

    def get_items(self, item):
        #self.object = object
        return item.objects.filter(company=self.pk).exclude(approved=False)

    def count_reviews(self):
        return self.get_reviews().count()

    def get_scores(self):
        output = {}
        for item in ('overallscore',
                     'advancement',
                     'worklife',
                     'compensation',
                     'environment',):
            output[item] = self.reviews.aggregate(score=Avg(item))['score']
            if output[item] is None:
                output[item] = 0
            else:
                output[item] = round(output[item], 1)
        return output 

    def get_scores_strings(self):
        """Returns human readable string of scores (e.g. for admin)"""
        scores = self.get_scores()
        string = ""
        for key, value in scores.items():
            string += "{:<25}: {:>4}\n".format(
                str(Review._meta.get_field(key).verbose_name), value)
        return string
        

class Position(models.Model):
        
    STATUS_ZATRUDNIENIA = [
        ('A', 'Pełen etat'),
        ('B', 'Część etatu'),
        ('C', 'Zlecenie'),
        ('D', 'Samozazatrudnienie'),
        ('E', 'Inne'),
    ]

    years = range(datetime.datetime.now().year, 1970, -1)
    YEARS = [(i, i) for i in years]
    months = range(1, 13)
    MONTHS = [(i, '{:02}'.format(i)) for i in months]
 
    date = models.DateTimeField(auto_now_add=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                             on_delete=models.SET_NULL)
    #company_name used to store name before entry is associated with a Company database record
    company_name = models.CharField(max_length=100, null=True, blank=True)
    company_linkedin_id=models.CharField(max_length=25, null=True)
    #company used to associate position with Company database record, blank before the association
    company = models.ForeignKey(Company, on_delete=models.SET_NULL,
                                blank=True, null=True)
    linkedin_id = models.PositiveIntegerField(blank=True, null=True)
    location = models.CharField(max_length=50, null=True)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100, blank=True, null=True)
    start_date_month = models.PositiveIntegerField(null=True,
                                                   choices=MONTHS, default=None)
    start_date_year = models.PositiveIntegerField(null=True,
                                                  choices=YEARS, default=None)
    employment_status = models.CharField(max_length=1,
                                         choices=STATUS_ZATRUDNIENIA,
                                         default='A')

    class Meta:
        verbose_name = "Stanowisko"
        verbose_name_plural = "Stanowiska"
    
    def __str__(self):
        if self.company:
            company = str(self.company)
        elif self.company_name:
            company = self.company_name
        else:
            company = ' '
        return self.position + ' - ' + company + ' - ' + self.user.email

class SelectedManager(models.Manager):

    use_for_related_fields = True

    def selected(self, company, **kwargs):
        return self.filter(**kwargs).exclude(approved=False)
    
class Review(ApprovableModel):

    RATINGS = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
        
    date = models.DateTimeField('data', auto_now_add=True, editable=False)
    company = models.ForeignKey(Company, verbose_name='firma',
                                on_delete=models.CASCADE, editable=False)
    position = models.ForeignKey(Position, verbose_name='stanowisko',
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True, editable=False)
    title = models.CharField('tytuł', max_length=100)
    pros = models.TextField('zalety')
    cons = models.TextField('wady')
    comment = models.TextField('co należy zmienić', blank=True)

    overallscore = models.PositiveIntegerField('ocena ogólna',
                                               choices=RATINGS, default=None)
    advancement = models.PositiveIntegerField('możliwości rozwoju',
                                              choices=RATINGS, default=None)
    worklife = models.PositiveIntegerField('równowaga praca/życie',
                                           choices=RATINGS, default=None)
    compensation = models.PositiveIntegerField('zarobki',
                                               choices=RATINGS, default=None)
    environment = models.PositiveIntegerField('atmosfera w pracy',
                                              choices=RATINGS, default=None)

    objects = SelectedManager()
    
    class Meta:
        verbose_name = "Opinia"
        verbose_name_plural = "Opinie"

    def __str__(self):
        return 'id_{}-{}-{}'.format(str(self.id), self.company.name, self.title)

    def get_absolute_url(self):
        return reverse('company_page',
                       kwargs={'pk': self.company.id})
    
    def get_scores(self):
        return {'overallscore': self.overallscore,
                'advancement': self.advancement,
                'worklife': self.worklife,
                'compensation': self.compensation,
                'environment': self.environment,
                }


class Salary(ApprovableModel):
    PERIOD = [
        ('M', 'miesięcznie'),
        ('K', 'kwartalnie'),
        ('R', 'rocznie'),
        ('G', 'na godzinę'),
    ]
    GROSS_NET = [
        ('G', 'brutto'),
        ('N', 'netto'),
    ]

    date = models.DateTimeField('data', auto_now_add=True, editable=False)
    company = models.ForeignKey(Company, verbose_name= 'firma',
                                on_delete=models.CASCADE, editable=False)
    position = models.ForeignKey(Position, verbose_name="stanowisko",
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True, editable=False)

    currency = models.CharField('waluta',
                                max_length=3, default='PLN')
    salary_input = models.PositiveIntegerField('pensja')
    period = models.CharField('',
                              max_length=1, default='M', choices=PERIOD,
                              )
    gross_net = models.CharField(
        '', max_length=1, default='G', choices=GROSS_NET)

    bonus_input = models.PositiveIntegerField('premia', default=0,
                                              blank=True, null=True)
    bonus_period = models.CharField('',
                                    max_length=1, default='R', choices=PERIOD,
                                    )
    bonus_gross_net = models.CharField('',
                                       max_length=1, default='G', choices=GROSS_NET,
                                       )

    base_monthly = models.PositiveIntegerField('Pensja zasadnicza miesięcznie',
                                               default=0, editable=False)
    base_annual = models.PositiveIntegerField('Pensja zasadnicza rocznie',
                                              default=0, editable=False)

    total_monthly = models.PositiveIntegerField('Pensja całkowita miesięcznie',
                                                default=0, editable=False)
    total_annual = models.PositiveIntegerField('Pensja całkowita rocznie',
                                               default=0, editable=False)

    class Meta:
        verbose_name = "Zarobki"
        verbose_name_plural = "Zarobki"

    def __str__(self):
        return 'id_{}_{}'.format(self.id, self.company)

    def get_absolute_url(self):
        return reverse('company_page',
                       kwargs={'pk': self.company.id})
        
    @staticmethod
    def convert(currency='PLN', period='M', gross_net='G', value=1):
        """
        Converts numbers input in different formats to comparable basis.
        """
        zus = 0.0976 + 0.015 #stawka emerytalna + rentowa
        ch = 0.0245 #stawka chorobowa
        z7 = 0.0775 #stawka ub. zdrowotnego odliczana od podatku
        z9 = 0.09 #stawka ub. zdrowotnego placona
        z = z9 - z7 #stawka zdrowotna nieodliczalna od podatku
        ku = 111.25 * 12 #koszty uzyskania przychodu
        kw = 556.02 #roczna kwota wolna od podatku
        step = 85528 #próg podatkowy
        limit_zus = 127890 #próg powyżej, którego nie płaci się zus
        r_1 = 0.18 #stawka podatku do progu podatkowego (step)
        r_2 = 0.32 #stawka powyzej progu podatkowego
        tax_1 = 15395.04 #podatek płacony przy brutto=step

        def gross_to_net(B):
            """
            Przelicza ROCZNE przychody brutto na dochód netto przy standardowej 
            umowie o pracę. Wynik zaokrąglony do najbliższej 100zl.
            """
            base = B * (1 - zus - ch) - ku
            if base < step:
                N = B*(1 - zus - ch)*(1 - z - r_1) + ku*r_1 + kw
            elif B <= limit_zus:
                N = B*(1 - zus - ch)*(1 - z - r_2) + (ku + step)*r_2 - tax_1 + kw
            else:
                N = 86620 + (B - limit_zus)*(1 - ch)*(1 - z - r_2)
                return round(N/100, 0) * 100

        def net_to_gross(N):
            """
            Przelicza ROCZNE dochody netto na przychód brutto przy standardowej
            umowie o pracę. Wynik zaokrąglony do najbliższej 100zl.
            """
            B = (N - ku*r_1 - kw) / ((1 - zus - ch)*(1 - z - r_1))
            base = B * (1 - zus - ch) - ku
            if base >= step:
                B = (N + tax_1 - kw - (ku + step)*r_2)/((1 - zus - ch)*(1 - z - r_2))
                if B > limit_zus: 
                    B = ((N - 86620)/((1 - ch)*(1 - z - r_2))) + limit_zus
            return round(B/100, 0) * 100
        
        if gross_net == 'N':
            return net_to_gross(value)
        

class Interview(ApprovableModel):
    HOW_GOT = [
        ('A', 'Ogłoszenie'),
        ('B', 'Kontakty profesjonalne'),
        ('C', 'Head-hunter'),
        ('D', 'Znajomi-rodzina'),
        ('E', 'Seks z decydentem'),
        ('F', 'Targi/prezentacje'),
        ('F', 'Inne'),
    ]
    DIFFICULTY = [
        (1, 'B. łatwo'),
        (2, 'Łatwo'),
        (3, 'Średnio'),
        (4, 'Trudno'),
        (5, 'B. trudno'),
    ]

    GOT_OFFER = [
        (True, 'Tak'),
        (False, 'Nie'),
        ]

    RATINGS = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, editable=False)
    position = models.CharField('stanowisko',
                                max_length=100)
    department = models.CharField('departament',
                                  max_length=100, blank=True)
    how_got = models.CharField('droga do interview',
                               max_length=1, choices=HOW_GOT, default=None)
    difficulty = models.PositiveIntegerField('trudność',
                                             choices=DIFFICULTY, default=None)
    got_offer = models.BooleanField('dostał ofertę',)
    questions = models.TextField('pytania', null=True, blank=True)
    impressions = models.TextField('wrażenia')
    rating = models.PositiveIntegerField('Ocena', choices=RATINGS, default=None)

    class Meta:
        verbose_name = "Rozmowa"
        verbose_name_plural = "Rozmowy"

    def __str__(self):
        return 'id_' + str(self.id) + '_' + str(self.company)

    def get_absolute_url(self):
        return reverse('company_page',
                       kwargs={'pk': self.company.id})

    def get_scores(self):
        """"Used by method calculating number of rating stars for display."""
        return {'rating': self.rating,
                }
