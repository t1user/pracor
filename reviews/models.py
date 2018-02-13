import datetime

from django.conf import settings
from django.db import models
from django.db.models import Avg, Max, Min, Count, Func
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from unidecode import unidecode

from .managers import SelectedManager, SalaryManager, ArrayAgg #modified version of ArrayAgg


class ApprovableModel(models.Model):
    """
    Abstract model providing features for entry approval in the admin module.
    """
    # approved set to False prevents the record from being displayed
    approved = models.NullBooleanField(
        'Zatwierdzone', default=None, null=True, blank=True)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Zatwierdzający',
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True, editable=False)
    reviewed_date = models.DateField('Data przeglądu', null=True, blank=True)

    class Meta:
        abstract = True


class Company(ApprovableModel):

    EMPLOYMENT = [('A', '<100'), ('B', '101-500'), ('C', '501-1000'),
                  ('D', '1001-5000'), ('E', '5001-10000'), ('F', '>10000')]

    # only three values are required - to make company creation easy for users
    name = models.CharField('nazwa', max_length=200, unique=True, db_index=True)
    headquarters_city = models.CharField('siedziba centrali', max_length=60)
    website = models.URLField('strona www', unique=True, db_index=True)

    # other fields are optional, to be filled-in by admins (rather than users)
    date = models.DateField('data dodania do bazy',
                            auto_now_add=True, editable=False)
    region = models.CharField(
        'województwo', max_length=40, blank=True, null=True)
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
        # get rid of '-sa', '-sp-z-oo' and '-sp-z-oo-sp-k' etc. endings
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
        return Review.objects.selected(company=self.pk).select_related('position').order_by('-date')

    @property
    def sum_reviews(self):
        return self.reviews.aggregate(Avg('overallscore'))
    
    @property
    def salaries(self):
        return Salary.objects.groups(company=self.pk).order_by('-salary_count')

    @property
    def salaries_count(self):
        return Salary.objects.groups(company=self.pk).count()

    @property
    def sum_salaries(self):
        """
        Return average, min and max of all annual salaries in the company as
        a dictionary.
        """
        return Salary.objects.sums(company=self.pk)
        
    @property
    def interviews(self):
        return Interview.objects.selected(company=self.pk).order_by('-date')

    @property
    def sum_interviews(self):
        """
        Return average interview rating for the company.
        """
        return self.interviews.aggregate(sum_avg=Avg('rating'))

    @property
    def benefits(self):
        """
        Return a list of pk's of all benefits that have been reported for the company.
        """
        benefits = self.salary_set.aggregate(
            benefits=ArrayAgg('benefits', distinct=True))
        return benefits['benefits']
    
    @property
    def scores(self):
        """
        Return average of all ratings for the company.
        """
        return  self.reviews.aggregate(
            overallscore = Avg('overallscore'),
            advancement = Avg('advancement'),
            worklife = Avg('worklife'),
            compensation = Avg('compensation'),
            environment = Avg('environment'),
            )
    
    @property
    def item_count(self):
        """
        Return number of Reviews, Salaries and Interviews for Company.
        Potentially used to save number of querries in templates.
        CURRENTLY NOT IN USE.
        """
        return Company.objects.filter(id=self.pk).aggregate(
            review = Count('review', distinct=True),
            salary = Count('salary', distinct=True),
            interview = Count('interview', distinct=True),
            )
    
    def get_scores_strings(self):
        """
        Return human readable string of scores (e.g. for admin)
        """
        string = ""
        for key, value in self.scores.items():
            if value is None:
                value = 0
            string += "{}:\t{}\n".format(
                str(Review._meta.get_field(key).verbose_name), round(value, 1))
        return string


class Position(models.Model):

    STATUS_ZATRUDNIENIA = [
        ('A', 'pełen etat'),
        ('B', 'część etatu'),
        ('C', 'praktyka'),
    ]
    year = timezone.now().year
    years = range(year, 1959, -1)
    YEARS = [(i, i) for i in years]
    YEARS_E = YEARS[:]
    YEARS_E.insert(0, (0, 'obecnie'))
    months = range(1, 13)
    MONTHS = [(i, '{:02}'.format(i)) for i in months]
    MONTHS_E = MONTHS[:]
    MONTHS_E.insert(0, ('', '--'))


    date = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # company_name used to store name before entry is associated with
    # Company database record
    company_name = models.CharField(max_length=100, null=True, blank=True)
    company_linkedin_id = models.CharField(
        max_length=25, null=True, blank=True)
    # company used to associate position with Company database record, blank
    # before the association
    company = models.ForeignKey(Company, on_delete=models.CASCADE,
                                blank=True, null=True)
    linkedin_id = models.PositiveIntegerField(blank=True, null=True)
    location = models.CharField(max_length=50, null=True)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100, blank=True, null=True)
    start_date_month = models.PositiveIntegerField(choices=MONTHS)
    start_date_year = models.PositiveIntegerField(choices=YEARS)
    end_date_month = models.PositiveIntegerField(null=True, blank=True, choices=MONTHS_E)
    end_date_year = models.PositiveIntegerField(choices=YEARS_E, default=0)
    employment_status = models.CharField(max_length=1,
                                         choices=STATUS_ZATRUDNIENIA,
                                         default='A')

    class Meta:
        verbose_name = "Stanowisko"
        verbose_name_plural = "Stanowiska"
        indexes = [
            models.Index(fields=['position', 'company']),
            models.Index(fields=['user', 'company'])
            ]

    def __str__(self):
        if self.company:
            company = str(self.company)
        elif self.company_name:
            company = self.company_name
        else:
            company = ' '
        if self.user:
            user = self.user.email
        else:
            user = ''
        return 'id {} - {} - {} - {}'.format(self.id, self.position, company, user)


class Review(ApprovableModel):

    RATINGS = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]

    date = models.DateTimeField('data', auto_now_add=True, editable=False,
                                db_index=True)
    company = models.ForeignKey(Company, verbose_name='firma',
                                on_delete=models.CASCADE, editable=False)
    position = models.OneToOneField(Position, verbose_name='stanowisko',
                                 on_delete=models.CASCADE, editable=False)
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

    @property
    def scores(self):
        return {'overallscore': self.overallscore,
                'advancement': self.advancement,
                'worklife': self.worklife,
                'compensation': self.compensation,
                'environment': self.environment,
                }


class Benefit(ApprovableModel):
    name = models.CharField(max_length=100, unique=True)
    core = models.BooleanField(default=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.SET_NULL, null=True, related_name='created_by')

    class Meta:
        verbose_name = 'benefit'
        verbose_name_plural = 'benefity'

    def __str__(self):
        return self.name

class Salary(ApprovableModel):
    PERIOD = [
        ('G', 'na godzinę'),
        ('D', 'dziennie'),
        ('T', 'tygodniowo'),
        ('M', 'miesięcznie'),
        ('K', 'kwartalnie'),
        ('R', 'rocznie'),
    ]
    GROSS_NET = [
        ('G', 'brutto'),
        ('N', 'netto'),
    ]
    CONTRACT = [
        ('A', 'umowa o pracę'),
        ('B', 'zlecenie/umowa o dzieło'),
        ('C', 'samozatrudnienie'),
    ]

    date = models.DateTimeField('data', auto_now_add=True, editable=False)
    company = models.ForeignKey(Company, verbose_name='firma',
                                on_delete=models.CASCADE, editable=False)
    position = models.OneToOneField(Position, verbose_name="stanowisko",
                                    on_delete=models.CASCADE,
                                    editable=False)

    currency = models.CharField('waluta', max_length=3, default='PLN')
    salary_input = models.PositiveIntegerField('pensja')
    period = models.CharField('', max_length=1, default='M', choices=PERIOD)
    gross_net = models.CharField('', max_length=1, default='G', choices=GROSS_NET)

    bonus_input = models.PositiveIntegerField('premia', blank=True, null=True)
    bonus_period = models.CharField('', max_length=1, null=True, choices=PERIOD)

    #this choice is currently not implemented, all input values are gross
    bonus_gross_net = models.CharField('', max_length=1, default='G', choices=GROSS_NET)

    #following values are calculated by save() and used in reports
    salary_gross_input_period = models.PositiveIntegerField('pensja brutto',
                                                            editable=False, default=0)
    salary_gross_annual = models.PositiveIntegerField('pensja brutto rocznie',
                                                      default=0, editable=False)
    bonus_gross_input_period = models.PositiveIntegerField('premia brutto',
                                                           null=True, editable=False)
    bonus_gross_annual = models.PositiveIntegerField('premia brutto rocznie', null=True,
                                                     editable=False)
    
    contract_type = models.CharField('rodzaj umowy', max_length=1, default='A', choices=CONTRACT)
    comments = models.CharField('uwagi', max_length=200, blank=True)
    benefits = models.ManyToManyField(Benefit, blank=True, verbose_name='benefity')

    
    objects = SalaryManager()

    class Meta:
        verbose_name = "Zarobki"
        verbose_name_plural = "Zarobki"
        indexes =[
            models.Index(fields=['company', 'position'])
            ]

    def __str__(self):
        return 'id_{}_{}'.format(self.id, self.company)

    def save(self, *args, **kwargs):
        self.convert()
        if self.bonus_input == None or self.bonus_input == 0:
            self.bonus_period = None
        #make sure that zeros are not counted as inputs with values
        if self.bonus_input == 0:
            self.bonus_input = None
            self.bonus_gross_input_period = None
            self.bonus_gross_annual = None
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('company_page',
                       kwargs={'pk': self.company.id})

    def convert(self):
        """
        Converts input numbers to comparable basis.
        """
        zus = 0.0976 + 0.015  # stawka emerytalna + rentowa
        ch = 0.0245  # stawka chorobowa
        z7 = 0.0775  # stawka ub. zdrowotnego odliczana od podatku
        z9 = 0.09  # stawka ub. zdrowotnego placona
        z = z9 - z7  # stawka zdrowotna nieodliczalna od podatku
        ku = 111.25 * 12  # koszty uzyskania przychodu
        kw = 556.02  # roczna kwota wolna od podatku
        step = 85528  # próg podatkowy
        limit_zus = 127890  # próg powyżej, którego nie płaci się zus
        r_1 = 0.18  # stawka podatku do progu podatkowego (step)
        r_2 = 0.32  # stawka powyzej progu podatkowego
        tax_1 = 15395.04  # podatek płacony przy brutto=step

        def gross_to_net(B, zus=zus, ch=ch, z=z, ku=ku, kw=kw):
            """
            Przelicza ROCZNE przychody brutto na dochód netto. Jeśli nie podano
            żadnych **kwargs to jest to standardowa umowa o pracę. W przeciwnym
            wypadku trzeba określić parametry, które są różne niż przy standardowej
            umowie o pracę.
            """

            #jeśli kwotę wolną podano w procentach, użyj podanej liczby,
            #w przeciwnym wypadku użyj liczby podanej kwotowo w założeniach
            if ku < 1:
                ku = ku * B * (1 - zus - ch)

            base = B * (1 - zus - ch) - ku
            if base < step:
                N = B * (1 - zus - ch) * (1 - z - r_1) + ku * r_1 + kw
            elif B <= limit_zus:
                N = B * (1 - zus - ch) * (1 - z - r_2) + \
                    (ku + step) * r_2 - tax_1 + kw
            else:
                N = 86620 + (B - limit_zus) * (1 - ch) * (1 - z - r_2)
            return N

        def net_to_gross(N, zus=zus, ch=ch, z=z, ku=ku, kw=kw):
            """
            Przelicza ROCZNE dochody netto na przychód brutto. Jeśli nie podano
            żadnych **kwargs to jest to standardowa umowa o pracę. W przeciwnym
            wypadku trzeba określić parametry, które są różne niż  przy standardowej
            umowie o pracę.
            """

            #jeśli kwotę wolną podano w procentach, użyj podanej liczby,
            #w przeciwnym wypadku użyj liczby podanej kwotowo w założeniach
            if ku < 1:
                B = (N - kw) / ((1 - zus - ch) * (1 - z - r_1 + .2 *r_1))
                ku = ku * B * (1 - zus - ch)
            else:
                B = (N - ku * r_1 - kw) / ((1 - zus - ch) * (1 - z - r_1))
            base = B * (1 - zus - ch) - ku

            if base >= step:
                B = (N + tax_1 - kw - (ku + step) * r_2) / \
                    ((1 - zus - ch) * (1 - z - r_2))
                if B > limit_zus:
                    B = ((N - 86620) / ((1 - ch) * (1 - z - r_2))) + limit_zus
            return B

        period_devisor = {
            'G': 2008, #number of work hours in 2018
            'D': 251, #number of work days in 2018
            'T': 52,
            'M': 12,
            'K': 4,
            'R': 1,
        }

        salary_annual = period_devisor[self.period] * self.salary_input

        #net to gross conversion
        if self.gross_net == 'N':
            self.salary_gross_annual = net_to_gross(salary_annual)
        else:
            self.salary_gross_annual = salary_annual
            
        self.salary_gross_input_period = round(self.salary_gross_annual /
                                               period_devisor[self.period], 0)

        if self.bonus_input:
            bonus_annual = period_devisor[self.bonus_period] * self.bonus_input
            if self.bonus_gross_net == 'N':
                salary_net_annual = gross_to_net(self.salary_gross_annual)
                total_comp_net_annual = bonus_annual + salary_net_annual
                total_comp_gross_annual = net_to_gross(total_comp_net_annual)
                self.bonus_gross_annual = total_comp_gross_annual - self.salary_gross_annual
            else:
                self.bonus_gross_annual = bonus_annual

            self.bonus_gross_input_period = round(self.bonus_gross_annual /
                                                  period_devisor[self.bonus_period], 0)


class Interview(ApprovableModel):
    HOW_GOT = [
        ('A', 'Ogłoszenie'),
        ('B', 'Kontakty zawodowe'),
        ('C', 'Head-hunter'),
        ('D', 'Znajomi/rodzina'),
        ('E', 'Seks z decydentem'),
        ('F', 'Targi/prezentacje'),
        ('G', 'Strona internetowa firmy'),
        ('H', 'Inne'),
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

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='user')
    position = models.CharField('stanowisko', max_length=100, db_index=True)
    department = models.CharField('departament', max_length=100, blank=True)
    how_got = models.CharField('droga do interview',
                               max_length=1, choices=HOW_GOT, default=None)
    difficulty = models.PositiveIntegerField('trudność',
                                             choices=DIFFICULTY, default=None)
    got_offer = models.BooleanField('dostał ofertę?',)
    questions = models.TextField('proces i pytania', null=True, blank=True)
    impressions = models.TextField('wrażenia')
    rating = models.PositiveIntegerField('ocena', choices=RATINGS, default=None)

    objects = SelectedManager()

    class Meta:
        verbose_name = "Rozmowa"
        verbose_name_plural = "Rozmowy"

    def __str__(self):
        return 'id_' + str(self.id) + '_' + str(self.company)

    def get_absolute_url(self):
        return reverse('company_page',
                       kwargs={'pk': self.company.id})

    @property
    def scores(self):
        """"Used by method calculating number of rating stars for display."""
        return {'rating': self.rating,}
    
