from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse

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
    redirect_view = 'searchcompany'

    def get(self, request, *args, **kwargs):
        search_results = None
        searchterm = kwargs.get('searchterm').replace('_', ' ')
        if searchterm:
            search_results = Company.objects.filter(name__icontains=searchterm)
            #self.initial = {'company_name': searchterm}
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name,
                      {'form': form,
                       'search_results': search_results,
                       'searchterm': searchterm})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            searchterm = form.cleaned_data['company_name'].replace(' ', '_')
            return HttpResponseRedirect(reverse(self.redirect_view,
                                                kwargs={'searchterm': searchterm}))
        return render(request, self.template_name, {'form': form})
