from django.http import HttpResponseRedirect 
from django.shortcuts import render, get_object_or_404
from django.views import View
from django import forms
from django.urls import reverse, reverse_lazy
from django.views.generic import (UpdateView, DeleteView, CreateView,
                                  ListView, DetailView)


from .models import Company, Salary, Review


class CompanySearchForm(forms.Form):
    company_name = forms.CharField(label="Wyszukaj firmę", max_length=100)

    
class CompanySearchView(View):
    form_class = CompanySearchForm
    initial = {}
    template_name = 'reviews/company_search_form.html'
    redirect_view = 'company_search'

    def get(self, request, *args, **kwargs):
        search_results = ''
        searchterm_joined = kwargs.get('searchterm')
        searchterm = searchterm_joined.replace('_', ' ')
        if searchterm:
            search_results = Company.objects.filter(name__icontains=searchterm)
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name,
                      {'form': form,
                       'search_results': search_results,
                       'searchterm': searchterm,
                       'searchterm_joined': searchterm_joined})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            searchterm = form.cleaned_data['company_name'].replace(' ', '_')
            return HttpResponseRedirect(reverse(self.redirect_view,
                                                kwargs={'searchterm': searchterm}))
        return render(request, self.template_name, {'form': form})


class CompanyDetailView(DetailView):
    model = Company
    template_name = 'reviews/company_view.html'
    context_object_name = 'company'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_count'] = self.object.get_reviews().count()
        context['salary_count'] = self.object.get_salaries().count()
        context['scores'] =  self.object.get_scores()
        if self.kwargs['item']:
            if self.kwargs['item'] == 'recenzje':
                context['reviews'] = self.object.get_reviews().all()
            elif self.kwargs['item'] == 'zarobki':
                context['salaries'] = self.object.get_salaries().all()
        else:
            context['review'] = self.object.get_reviews().last()
            context['salary'] = self.object.get_salaries().last()
        return context

class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'headquarters_city', 'website']

    def clean_website(self):
        """
        Method cleans field: 'website'. Ensures that urls with http, https, 
        with and without www are treated as one.
        """
        url = self.cleaned_data['website']
        if url.startswith('https'):
            url = url.replace('https', 'http')
        if not url.startswith('http://www.'):
            url = url.replace('http://', 'http://www.')
        ### TODO check here if the website returns 200
        return url
"""
    def clean(self):
        data = super().clean()
        print(data)
"""

class CompanyCreate(CreateView):
    model = Company
    form_class = CompanyCreateForm
    initial = {'website': 'http://www.'}
    
    def get(self, request, **kwargs):
        company_name_joined = self.kwargs.get('company')
        company_name = company_name_joined.replace('_', ' ').title()
        self.initial['name'] = company_name
        return super().get(request, **kwargs)
    
    def form_valid(self, form):
        form.instance.headquarters_city = form.instance.headquarters_city.title()
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        """
        In case there's an attempt to create a non-unique Company,
        the method pulls out the instance(s) of the Company(s)
        that already exist(s) and adds it/them to the context.
        """
        context = self.get_context_data(**kwargs)
        context['form'] = form
        errorlist = form.errors.as_data()
        form_dict = form.instance.__dict__
        companies = []
        for field, errors in errorlist.items():
            for error in errors:
                if error.code == 'unique':
                    company = Company.objects.get(**{field: form_dict[field]})
                    if company not in companies:
                        companies.append(company)
        context['unique_error'] = companies
        return self.render_to_response(context)

    
class CompanyUpdate(UpdateView):
    model = Company
    fields = ['name', 'headquarters_city', 'website']
    #template_name = 'reviews/company_view.html'

    
class CompanyDelete(DeleteView):
    model = Company
    success_url = reverse_lazy('home')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['position', 'city', 'years_at_company', 'advancement',
                  'worklife', 'compensation', 'environment', 'overallscore',
                  'pros', 'cons', 'comment']

        labels = {
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

        widgets = {
            'advancement': forms.RadioSelect(),
            'worklife': forms.RadioSelect(),
            'compensation': forms.RadioSelect(),
            'environment': forms.RadioSelect(),
            'overallscore': forms.RadioSelect()
        }

            
class ReviewCreate(CreateView):
    form_class = ReviewForm
    model = Review 
    
    def form_valid(self, form):
        company = get_object_or_404(Company, pk=self.kwargs['id'])
        form.instance.company = company
        company.overallscore += form.instance.overallscore
        company.advancement += form.instance.advancement
        company.worklife += form.instance.worklife
        company.compensation += form.instance.compensation
        company.environment += form.instance.environment
        company.number_of_reviews += 1
        company.save(update_fields=['overallscore',
                                    'advancement',
                                    'worklife',
                                    'compensation',
                                    'environment',
                                    'number_of_reviews',
        ])
        form.instance.position = form.instance.position.title()
        form.instance.city = form.instance.city.title()
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_name'] = get_object_or_404(Company, pk=self.kwargs['id'])
        context['radios'] = ['overallscore', 'advancement', 'compensation', 'environment', 'worklife']
        return context


class SalaryCreate(CreateView):
    model = Salary
    fields = [
        'position',
        'city',
        'years_at_company',
        'employment_status',
        'currency',
        'salary_input',
        'period',
        'gross_net',
        'bonus_input',
        'bonus_period',
        'bonus_gross_net',
    ]

    def form_valid(self, form):
        form.instance.company = get_object_or_404(Company, pk=self.kwargs['id'])
        form.instance.years_experience = 5 #stub value to be replaced with request.user.something
        form.instance.city = form.instance.city.title()
        form.instance.position = form.instance.position.title()
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_name'] = get_object_or_404(Company, pk=self.kwargs['id'])
        return context

class CompanyList(ListView):
    model = Company
    context_object_name = 'company_list'
