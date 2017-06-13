from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from .models import Company
from .forms import CompanysearchForm, ReviewForm, SalaryForm

class BaseFormView(View):
    form_class = []
    initial = {'key': 'value'}
    template_name = 'form_template.html'
    redirect_view = 'home'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            self.process_result(request, form=form)
            return redirect(self.redirect_view)
        return render(request, self.template_name, {'form': form})

    def process_result(self, request, *args, **kwargs):
        pass


class ReviewView(BaseFormView):
    form_class = ReviewForm
    initial = {}
    template_name = 'reviews/review.html'
    redirect_view = 'home'

    def process_result(self, request, *args, **kwargs):
        form = kwargs.get('form')
        form.save()
        

class CompanysearchView(BaseFormView):
    form_class = CompanysearchForm
    initial = {}
    template_name = 'reviews/companysearchform.html'
    redirect_view = 'searchcompany_results'
    
    def process_result(self, request, *args, **kwargs):
        search_term = kwargs.get('form').cleaned_data['company_name']
        self.initial = search_term
        self.search_results = Company.objects.filter(name__icontains=search_term)
        print(search_term)
        print(self.search_results)
        
class CompanysearchResultsView(CompanysearchView):
    form_class = CompanysearchForm
    initial = {}
    template_name = 'reviews/companysearchform.html'
    redirect_view = 'searchcompany_results'
    search_results = {}

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form,
                                                    'search_results': self.search_results})
    
    def process_result(self, request, *args, **kwargs):
        search_term = kwargs.get('form').cleaned_data['company_name']
        self.initial = search_term
        self.search_results = Company.objects.filter(name__icontains=search_term)
        print(search_term)
        print(self.search_results)
        
        
        
        
