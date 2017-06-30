from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse, reverse_lazy
from django.views.generic import (UpdateView, DeleteView, CreateView,
                                  ListView, DetailView)
#from django.views.generic.detail import DetailView

from .models import Company, Salary, Review
from .forms import (CompanySearchForm, ReviewForm, SalaryForm,
                    CompanyForm)

"""
class BaseFormView(View):
    form_class = []
    initial = {'key': 'value'}
    template_name = 'form_template.html'
    redirect_view = 'home'
    redirect_data = None
    paras = None #parameters passed by urlconf
    context = {}
    
    def get_paras(self, *args, **kwargs):
        id = kwargs.get('id')
        print('id: ', id)
        if id:
            self.paras = Company.objects.get(pk=id)
            self.context['paras'] = self.paras

    def get(self, request, *args, **kwargs):
        self.get_paras(*args, **kwargs)
        print('initializing method GET with id: ', self.paras)
        print('Object: ', self)
        self.form = self.form_class(initial=self.initial)
        self.set_context()
        print(self.context)
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        self.get_paras(*args, **kwargs)
        print('initializing method POST with id: ', self.paras)
        print('Object: ', self)
        self.form = self.form_class(request.POST)
        if self.form.is_valid():
            # <process form cleaned data>
            self.process_result(request)
            if self.redirect_data:
                return redirect(self.redirect_view,
                                self.redirect_data)
            else:
                return redirect(self.redirect_view)
        self.set_context()
        return render(request, self.template_name, self.context)

    def set_context(self, *args, **kwargs):
        self.context['form'] = self.form
        for k, v in kwargs.items():
            self.context[k] = v
    
    def process_result(self, request, *args, **kwargs):
        self.model_instance = self.form.save()


class ReviewView(BaseFormView):
    form_class = ReviewForm
    template_name = 'reviews/review.html'
    redirect_view = 'company_page'

    def process_result(self, request, *args, **kwargs):
        incomplete_form = self.form.save(commit=False)
        incomplete_form.company = self.paras
        model_instance = self.form.save()
        self.redirect_data = model_instance.company.pk

class CompanyCreateView(BaseFormView):
    form_class = CompanyForm
    initial = {'website': 'http://www.'}
    template_name = 'reviews/create_company.html'
    company_name_joined = ''
    redirect_view = 'review'

    def get(self, request, *args, **kwargs):
        self.company_name_joined = kwargs.get('company')
        company_name = self.company_name_joined.replace('_', ' ')
        self.initial['name'] = company_name
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def process_result(self, request, *args, **kwargs):
        super().process_result(request, *args, **kwargs)
        self.redirect_data = self.model_instance.pk
"""
        
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
        context['review_count'] = self.object.review_set.count()
        context['salary_count'] = self.object.salary_set.count()
        if self.kwargs['item']:
            if self.kwargs['item'] == 'recenzje':
                context['reviews'] = self.object.review_set.all()
            elif self.kwargs['item'] == 'zarobki':
                context['salaries'] = self.object.salary_set.all()
        else:
            context['review'] = self.object.review_set.last()
            context['salary'] = self.object.salary_set.last()
        return context

    
class CompanyCreate(CreateView):
    model = Company
    initial = {'website': 'http://www.'}
    fields = ['name', 'headquarters_city', 'website']
    
    def get(self, request, **kwargs):
        company_name_joined = self.kwargs.get('company')
        company_name = company_name_joined.replace('_', ' ').title()
        self.initial['name'] = company_name
        return super().get(request, **kwargs)
        
    
class CompanyUpdate(UpdateView):
    model = Company
    fields = ['name', 'headquarters_city', 'website']
    #template_name = 'reviews/company_view.html'

    
class CompanyDelete(DeleteView):
    model = Company
    success_url = reverse_lazy('home')


class ReviewCreate(CreateView):
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

    def form_valid(self, form):
        form.instance.company = Company.objects.get(pk=self.kwargs['id'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_name'] = Company.objects.get(pk=self.kwargs['id'])
        return context


class SalaryCreate(CreateView):
    model = Salary
    fields = ['position', 'city', 'years_at_company', 'employment_status', 'salary']

    def form_valid(self, form):
        form.instance.company = Company.objects.get(pk=self.kwargs['id'])
        form.instance.years_experience = 5 #stub value to be replaced with request.user.something
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_name'] = Company.objects.get(pk=self.kwargs['id'])
        return context

class CompanyList(ListView):
    model = Company
    context_object_name = 'company_list'
