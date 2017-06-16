from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse


from django.views.generic.detail import DetailView

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


def companyview(request, pk):
    a = Company.objects.get(pk=pk)
    return HttpResponse(a)


class CompanyDetailView(DetailView):

    model = Company
    template_name = 'reviews/company_view.html'
    context_object_name = 'company'

'''
    def get_queryset(self, **kwargs):
        self.company = get_object_or_404(Company, pk=self.kwargs['pk'])
        return self.company
'''
