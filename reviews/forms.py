from django import forms
from django.forms import ModelForm
from .widgets import RadioSelectModified, RadioReversed

from .models import Review, Salary, Interview, Company, Position



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
"""
    def clean_company_name(self):
        data = self.cleaned_data.get('company_name')
        if data in QS_CHOICES:
            try:
                data = MyModel.objects.get(id=data)
            except MyModel.DoesNotExist:
                raise forms.ValidationError('foo')
        return data
"""

class CompanySelectFormOld(forms.Form):
    """
    NOT IN USE.
    Creates a RadioSelect with options given in kwarg 'companies' plus empty_label.
    """
    #queryset is a required parameter, so here an empty queryset is passed
    company_name = forms.ModelChoiceField(widget=RadioReversed(),
                                          queryset=Company.objects.none(),
                                          empty_label='Na liście nie ma firmy, w której pracuję',
                                          label='',
                                          )
    
    def __init__(self, *args, **kwargs):
        self.companies = kwargs.pop('companies')
        super().__init__(*args, **kwargs)
        self.fields['company_name'].queryset = self.companies

    
    
class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'headquarters_city', 'website']

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

        labels = {
            'position': 'stanowisko',
            'department': 'departament',
            'location': 'miasto',
            'start_date_year': 'rok',
            'start_date_month': 'miesiąc',
            'employment_status': 'rodzaj umowy',
            }

        widgets = {
            'start_date_year': forms.Select(attrs={'class':'inline'}),
            'start_date_month': forms.Select(attrs={'class':'inline'}),
            }
        
        """
        help_texts = {
            'start_date_year': 'rok',
            'start_date_month': 'miesiąc',
            }
        """
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'advancement',
                  'worklife', 'compensation', 'environment', 'overallscore',
                  'pros', 'cons', 'comment']

        labels = {
            'title': 'tytuł recenzji',
            'advancement': 'możliwości rozwoju',
            'worklife': 'równowaga praca/życie',
            'compensation': 'zarobki',
            'environment': 'atmosfera w pracy',
            'pros': 'zalety',
            'cons': 'wady',
            'ovarallscore': 'ocena ogólna',
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

class SalaryForm(forms.ModelForm):
    #period = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'inline',}))
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
            'salary_input': forms.NumberInput(attrs={'step': 100, 'value': 2000,
                                                     'class': 'inline'}),
            'period': forms.Select(attrs={'class': 'inline'}),
            'gross_net': forms.Select(attrs={'class': 'inline'}),
            
            'bonus_input': forms.NumberInput(attrs={'step': 1000, 'class': 'inline'}),
            'bonus_period': forms.Select(attrs={'class': 'inline',}),
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
    # this override is necessary as otherwise 'required' attr is not properly generated
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

        widgets = {
            'difficulty': forms.RadioSelect(),
            'impressions': forms.Textarea(),
            #'got_offer': forms.RadioSelect(),
            'rating': RadioSelectModified(),
            }

        """help_texts = {
            'difficulty': '1 - bardzo łatwo, 5 - bardzo trudno',
            }"""
