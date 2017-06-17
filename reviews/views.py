from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse


from django.views.generic.detail import DetailView

from .models import Company
from .forms import (CompanysearchForm, ReviewForm, SalaryForm,
                    CompanyForm)


class BaseFormView(View):
    form_class = []
    initial = {'key': 'value'}
    template_name = 'form_template.html'
    redirect_view = 'home'
    model_instance = None

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            self.process_result(request, form=form)
            return redirect(self.redirect_view,
                            self.model_instance.pk)
        return render(request, self.template_name, {'form': form})

    def process_result(self, request, *args, **kwargs):
        pass


class ReviewView(BaseFormView):
    form_class = ReviewForm
    initial = {}
    template_name = 'reviews/review.html'
    redirect_view = 'searchcompany'

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        if id:
            company = Company.objects.get(pk=id)
        # self.
        super().get(self, request, *args, **kwargs)

    def process_result(self, request, *args, **kwargs):
        form = kwargs.get('form')
        self.model_instance = form.save()


class CompanysearchView(BaseFormView):
    form_class = CompanysearchForm
    initial = {}
    template_name = 'reviews/companysearchform.html'
    redirect_view = 'searchcompany'

    def get(self, request, *args, **kwargs):
        search_results = None
        searchterm_joined = kwargs.get('searchterm')
        searchterm = searchterm_joined.replace('_', ' ')
        if searchterm:
            search_results = Company.objects.filter(name__icontains=searchterm)
            # self.initial = {'company_name': searchterm}
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


class CompanyCreateView(ReviewView):
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
