from itertools import chain

from django import forms
from django.forms import ModelForm
from django.db.models import Q

from .models import Company, Interview, Position, Review, Salary, Benefit
from .widgets import RadioReversed, RadioSelectModified
from .validators import ProfanitiesFilter, TextLengthValidator



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
                  'start_date_year', 'start_date_month', 'end_date_year', 'end_date_month',
                  'employment_status',]

        field_classes = {
            'position': CensoredField,
            'department': CensoredField,
            'location': CensoredField,
        }

        #start date and end date labels added through css
        labels = {
            'position': 'stanowisko',
            'department': 'departament',
            'location': 'miasto',
            'start_date_year': 'rok',
            'start_date_month': 'miesiąc',
            'end_date_year': 'rok',
            'end_date_month': 'miesiąc',
            'employment_status': 'rodzaj umowy',
        }

        widgets = {
            'start_date_year': forms.Select(attrs={'class': 'inline'}),
            'start_date_month': forms.Select(attrs={'class': 'inline'}),
            'end_date_year': forms.Select(attrs={'class': 'inline'}),
            'end_date_month': forms.Select(attrs={'class': 'inline'}),
        }

        help_texts = {
            'department': 'Jeśli nie możesz podać dokładnej nazwy departamentu, określ obszar, np: kadry, finanse, oddział xyz, itp.',
        }

    def __init__(self, *args, **kwargs):
        #request and company are required by Salary form and obsolete here
        if 'request' in kwargs:
            kwargs.pop('request')
        if 'company' in kwargs:
            kwargs.pop('company')
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
        min_length = 20 #number of words required in the field
        self.fields['pros'].validators.append(TextLengthValidator(min_length))
        self.fields['cons'].validators.append(TextLengthValidator(min_length))


class SalaryForm(forms.ModelForm):
    other = CensoredField(label='Inne benefity',
                            help_text='Opcjonalnie, wymień po przecinku inne benefity, które Ci przysługują poza tymi na liście')
    
    class Meta:
        model = Salary
        fields = [
            #'currency', currently not implemented
            'salary_input',
            'period',
            #'gross_net', currently not implemented, all inputs gross
            'bonus_input',
            'bonus_period',
            #'bonus_gross_net', currently not implemented, all inputs gross
            'contract_type',
            'comments',
            'benefits',
            'other'
        ]
        widgets = {
            'currency': forms.TextInput(attrs={'size': 3}),
            'salary_input': forms.NumberInput(attrs={'class': 'inline'}),
            'period': forms.Select(attrs={'class': 'inline'}),
            'gross_net': forms.Select(attrs={'class': 'inline'}),

            'bonus_input': forms.NumberInput(attrs={'class': 'inline break_before'}),
            'bonus_period': forms.Select(attrs={'class': 'inline', }),
            'bonus_gross_net': forms.Select(attrs={'class': 'inline'}),
            'benefits': forms.CheckboxSelectMultiple(),
        }

        labels = {
            'salary_input': 'Pensja brutto',
            'bonus_input': 'Premia brutto',
            }

        help_texts = {
            'comments': 'Wszelkie uwagi, które dodatkowo określają charakter otrzymywanego wynagrodznia. Uwagi te nie zostaną opublikowane',
            'benefits': 'Zaznacz benefity, które Ci przysługują',
            }


    def __init__(self, request, company, *args, **kwargs):
        """
        Override to avoid displaying 'required' asterics next to
        certain fields and limit options displayed in 'benefits'
        field to core and those previously mentioned for 
        the company.
        """
        super().__init__(*args, **kwargs)
        self.request = request
        self.company = company
        #choose only core items or relevant to the company
        extra_benefits = self.company.benefits
        self.fields['benefits'].queryset = Benefit.objects.filter(
            Q(core=True) | Q(pk__in=extra_benefits)
            )
                                                               
        self.fields['period'].required = False
        #self.fields['gross_net'].required = False
        self.fields['bonus_period'].required = False
        #self.fields['bonus_gross_net'].required = False
        self.fields['other'].required = False


    def clean_other(self):
        other_benefit_list = self.cleaned_data['other'].split(',')
        new_benefits_list = []
        existing_benefits = Benefit.objects.filter(name__in=other_benefit_list)
        for existing in existing_benefits:
            other_benefit_list.remove(existing.name)
        for benefit in other_benefit_list:
            benefit = benefit.strip()
            if benefit == '':
                continue
            new_benefit = Benefit.objects.create(name=benefit,
                                   author=self.request.user,
            )
            new_benefits_list.append(new_benefit)
        return chain(new_benefits_list, existing_benefits)



 
    def clean(self):
        cleaned_data = super().clean()
        if 'other' in cleaned_data.keys():
            benefits = cleaned_data['benefits']
            other = cleaned_data['other']
            cleaned_data['benefits'] = chain(benefits, other)
        return cleaned_data

    




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


    def clean_position(self):
        return self.cleaned_data['position'].title()

    def clean_department(self):
        if self.cleaned_data['department']:
            return self.cleaned_data['department'].title()


class ContactForm(forms.Form):
    your_email = forms.EmailField(label='Twój email',)
    subject = forms.CharField(label='Temat', strip=True)
    message = forms.CharField(label='Wiadomość', strip=True, widget=forms.Textarea())

    
