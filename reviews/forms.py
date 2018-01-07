import csv
import re

from django import forms
#from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Company, Interview, Position, Review, Salary
from .widgets import RadioReversed, RadioSelectModified


class CompanySearchForm(forms.Form):
    company_name = forms.CharField(label="Wyszukaj firmę", max_length=100)


class CompanySelectForm(forms.Form):
    company_name = forms.ChoiceField(widget=forms.RadioSelect(), label='')
    position = forms.CharField(max_length=30, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.companies = kwargs.pop('companies')
        super().__init__(*args, **kwargs)
        self.fields['company_name'].choices = (list(self.companies) +
                                               [('None', 'Na liście nie ma firmy, w której pracuję')])

        
class ProfanitiesFilter():
    """
    Custom validator to filter out swear words.
    First file has words that are matched inside other words.
    Second file has words that are matched only as full words.
    """
    #makeing those class variables ensures this code is called only once - after
    #starting server
    words = ''
    with open('reviews/profanities_filter/prof_fil_broad.txt') as f:
        i = csv.reader(f, delimiter='\n')
        for item in i:
            words += item[0]
            words += '|'

    more_words = ''
    with open('reviews/profanities_filter/prof_fil.txt') as f:
        i = csv.reader(f, delimiter='\n')
        for item in i:
            text_item = '\\b{}\\b|'.format(item[0])
            more_words += text_item

    words += more_words
    pattern = re.compile(words, re.IGNORECASE)

    def __call__(self, value):
        matches = self.pattern.findall(value)
        matches = [match for match in matches if match != '']
        full_words = value.split(' ')
        full_matched_words = []
        for word in full_words:
            for match in matches:
                if match in word:
                    full_matched_words.append(word.lower().rstrip(',!?:;.'))
        matches = set(full_matched_words)
        # if partial words matched, get the full words, of which they are part
        if matches:
            if len(matches) == 1:
                value = ''.join(matches)
            else:
                value = ', '.join(matches)
            raise forms.ValidationError('Niedopuszczalne wyrażenia: {}'.format(value),
                                        params={'value': value},
                                        )


class CensoredField(forms.CharField):
    """
    Standard CharField with custom validator filtering out profanities.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(ProfanitiesFilter())


class CompanyCreateForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ['name', 'headquarters_city', 'website']

        field_classes = {
            'name': CensoredField,
            'headquarters_city': CensoredField,
        }

    def clean_name(self):
        return self.cleaned_data['name'].title()
        
    def clean_headquarters_city(self):
        return self.cleaned_data['headquarters_city'].title()

    def clean_website(self):
        """Clean field: 'website', ensure that urls with http, https, 
        with and without www are treated as the same."""
        url = self.cleaned_data['website']
        if url.startswith('https'):
            url = url.replace('https', 'http')
        if not url.startswith('http://www.'):
            url = url.replace('http://', 'http://www.')
        # TODO check here if the website returns 200
        return url


class PositionForm(forms.ModelForm):

    class Meta:
        model = Position
        fields = ['position', 'department', 'location',
                  'start_date_year', 'start_date_month', 'employment_status']

        field_classes = {
            'position': CensoredField,
            'department': CensoredField,
            'location': CensoredField,
        }

        labels = {
            'position': 'stanowisko',
            'department': 'departament',
            'location': 'miasto',
            'start_date_year': 'rok',
            'start_date_month': 'miesiąc',
            'employment_status': 'rodzaj umowy',
        }

        widgets = {
            #'position': forms.TextInput(attrs={'class': 'auto-position'}),
            #'department': forms.TextInput(attrs={'class': 'auto-position'}),
            #'location': forms.TextInput(attrs={'class': 'auto-position'}),
            'start_date_year': forms.Select(attrs={'class': 'inline'}),
            'start_date_month': forms.Select(attrs={'class': 'inline'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['position'].widget.attrs['class'] = 'auto-position'
        self.fields['department'].widget.attrs['class'] = 'auto-position'
        self.fields['location'].widget.attrs['class'] = 'auto-position'

    def clean_position(self):
        return self.cleaned_data['position'].title()

    def clean_department(self):
        if self.cleaned_data['department']:
            return self.cleaned_data['department'].title()

    def clean_location(self):
        return self.cleaned_data['location'].title()


class TextLengthValidator():
    """
    Verify whether user input meets the minimum length requirement.
    """
    def __init__(self, requirement=20):
        self.req = requirement
        
    def __call__(self, text):
        words = text.split(' ')
        length = len(words)
        if length < self.req:
            miss = self.req - length
            raise forms.ValidationError(
                'Za krótki wpis, wymagane {req} słow (brakuje {miss})'.format(
                    miss=miss, req=self.req), code='invalid')

        
class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['title', 'advancement',
                  'worklife', 'compensation', 'environment', 'overallscore',
                  'pros', 'cons', 'comment']

        field_classes = {
            'title': CensoredField,
            'pros': CensoredField,
            'cons': CensoredField,
            'overallscore': CensoredField,
            'comment': CensoredField,
        }

        labels = {
            'title': 'tytuł recenzji',
            'advancement': 'możliwości rozwoju',
            'worklife': 'równowaga praca/życie',
            'compensation': 'zarobki',
            'environment': 'atmosfera w pracy',
            'pros': 'zalety',
            'cons': 'wady',
            'overallscore': 'ocena ogólna',
            'comment': 'co należy zmienić?',
        }

        widgets = {
            'advancement': RadioSelectModified(),
            'worklife': RadioSelectModified(),
            'compensation': RadioSelectModified(),
            'environment': RadioSelectModified(),
            'overallscore': RadioSelectModified(),
            'pros': forms.Textarea(),
            'cons': forms.Textarea(),
            'comment': forms.Textarea(),
        }

        help_texts = {
            'title': 'Jedno zdanie podsumowujące opinię',
            'pros': 'Minimum 20 słów (2-3 zdania). Konieczne by opinia była wyważona.',
            'cons': 'Minimum 20 słów (2-3 zdania). Konieczne by opinia była wyważona.',
            'comment': 'Inne uwagi o tym co mogłoby sprawić, że praca w tej firmie byłaby lepsza.',
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        min_length = 20
        self.fields['pros'].validators.append(TextLengthValidator(min_length))
        self.fields['cons'].validators.append(TextLengthValidator(min_length))


class SalaryForm(forms.ModelForm):

    class Meta:
        model = Salary
        fields = [
            'currency',
            'salary_input',
            'period',
            'gross_net',
            'bonus_input',
            'bonus_period',
            'bonus_gross_net',
        ]
        widgets = {
            'currency': forms.TextInput(attrs={'size': 3}),
            'salary_input': forms.NumberInput(attrs={'class': 'inline'}),
            'period': forms.Select(attrs={'class': 'inline'}),
            'gross_net': forms.Select(attrs={'class': 'inline'}),

            'bonus_input': forms.NumberInput(attrs={'step': 1000, 'class': 'inline'}),
            'bonus_period': forms.Select(attrs={'class': 'inline', }),
            'bonus_gross_net': forms.Select(attrs={'class': 'inline'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Override to avoid displaying 'required' asterics next to
        certain fields.
        """
        super().__init__(*args, **kwargs)
        self.fields['period'].required = False
        self.fields['gross_net'].required = False
        self.fields['bonus_period'].required = False
        self.fields['bonus_gross_net'].required = False


class InterviewForm(forms.ModelForm):
    # this override is necessary as otherwise 'required' attr is not properly
    # generated
    got_offer = forms.TypedChoiceField(required=True, label="Czy dostałaś/eś ofertę?",
                                       choices=((True, 'Tak'), (False, 'Nie')),
                                       widget=forms.RadioSelect(
                                           choices=((True, 'Tak'), (False, 'Nie'))),
                                       )

    class Meta:
        model = Interview
        fields = [
            'position',
            'department',
            'how_got',
            'difficulty',
            'got_offer',
            'questions',
            'impressions',
            'rating',
        ]

        field_classes = {
            'position': CensoredField,
            'department': CensoredField,
            'how_got': CensoredField,
            'questions': CensoredField,
            'impressions': CensoredField,
        }

        widgets = {
            'difficulty': forms.RadioSelect(),
            'impressions': forms.Textarea(),
            'rating': RadioSelectModified(),
        }

        help_texts = {
            'department': 'Jeśli nie możesz podać dokładnej nazwy departamentu, określ obszar, np: kadry, finanse, oddział xyz, itp.',
            'how_got': 'Skąd dowiedziałaś/łeś się o wolnym stanowisku, jak trafiłaś/łeś do firmy.',
            'questions': 'Jak przebiegał proces rekrutacyjny i jakie pytania zadano na różnych jego etapach.',
            'impressions': 'Pozytywne i negatywne strony procesu rekrutacyjnego.',
            'rating': 'Jak oceniasz całość doświadczenia rekrutacyjnego w firmie.',
            }
