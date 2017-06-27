from django import forms
from django.forms import ModelForm
from .models import Review, Salary, Company


class CompanySearchForm(forms.Form):
    company_name = forms.CharField(label="Wyszukaj firmę", max_length=100)


class ReviewForm(ModelForm):

    class Meta:
        model = Review
        fields = [#'company',
                  'position', 'city', 'years_at_company', 'advancement',
                  'worklife', 'compensation', 'environment', 'overallscore',
                  'pros', 'cons', 'comment']
        labels = {
            #'company': 'firma',
            'position': 'stanowisko',
            'city': 'miasto',
            'years_at_company': 'staż w firmie',
            'advancement': 'możliwości rozwoju',
            'worklife': 'równowaga praca/życie',
            'compensation': 'zarobki',
            'environment': 'atmosfera w pracy',
            'pros': 'zalety',
            'cons': 'wady',
            'ovarallscore': 'ocena ogólna',
            'comment': 'dodatkowe uwagi',
        }
        help_text = {
            #'company': 'Firma, której dotyczy recenzja',
            'position': 'Ostatnie/obecne stanowisko w firmie',
        }


class SalaryForm(ModelForm):

    class Meta:
        model = Salary
        fields = ['company', 'position', 'city', 'years_at_company',
                  'years_experience', 'employment_status', 'salary']


class CompanyForm(ModelForm):

    class Meta:
        model = Company
        fields = ['name', 'headquarters_city', 'website']
        initial = {
            'website': 'http://',
        }
