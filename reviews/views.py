from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views import View
from django import forms
from django.urls import reverse, reverse_lazy
from django.views.generic import (UpdateView, DeleteView, CreateView,
                                  ListView, DetailView)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .widgets import RadioSelectModified

from .models import Company, Salary, Review, Interview


class CompanySearchForm(forms.Form):
    company_name = forms.CharField(label="Wyszukaj firmę", max_length=100)


class HomeView(View):
    form_class = CompanySearchForm
    template_name = 'reviews/home.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name,
                      {'form': form})


class CompanySearchView(View):
    form_class = CompanySearchForm
    initial = {}
    template_name = 'reviews/home.html'
    redirect_template_name = 'reviews/company_search_results.html'
    redirect_view = 'company_search'

    def get(self, request, *args, **kwargs):
        search_results = ''
        searchterm_joined = kwargs.get('searchterm')
        searchterm = searchterm_joined.replace('_', ' ')
        if searchterm:
            search_results = Company.objects.filter(name__icontains=searchterm)
            self.template_name = self.redirect_template_name
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


class CompanyDetailView(LoginRequiredMixin, DetailView):
    model = Company
    template_name = 'reviews/company_view.html'
    context_object_name = 'company'
    item_data = {'review':
                 {'object': Review,
                  'name': 'recenzje',
                  'file': 'reviews/review_item.html',
                  },
                 'salary':
                 {'object': Salary,
                     'name': 'zarobki',
                     'file':  'reviews/salary_item.html',
                  },
                 'interview':
                 {'object': Interview,
                     'name': 'interview',
                     'file':  'reviews/interview_item.html',
                  },
                 }

    def get_items(self, **kwargs):
        items = {}
        for key, value in self.item_data.items():
            object = self.object.get_objects(value['object'])
            count = object.count()
            last = object.last()
            try:
                scores = last.get_scores()
                stars = self.get_stars(scores)
            except:
                stars = {}
            name = value['name']
            file = value['file']
            items[key] = {'count': count,
                          'last': last,
                          'name': name,
                          'file': file,
                          'stars': stars,
                          }
        return items

    def get_stars(self, scores):
        """Calculate number of full, half and blank rating stars for a given dictionary of scores. The dictionary 'scores' has to be in the format:
        {'overallscore': overallscore,
         'advancement': advancement,
         'worklife': worklife,
         'compensation': compensation,
         'environment': environment,} """
        rating_items = {}
        for key, value in scores.items():
            truncated = int(value)
            half = value - truncated
            if 0.25 <= half < 0.75:
                half = 1
            else:
                half = 0
            if value - truncated >= 0.75:
                truncated += 1
            full = range(truncated)
            blank = range(5 - truncated - half)
            # add field names to context to allow for looping over rating
            # items
            label = self.object._meta.get_field(key).verbose_name
            rating_items[key] = {'rating': value,
                                 'full': full,
                                 'half': half,
                                 'blank': blank,
                                 'label': label}
        return rating_items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scores = self.object.get_scores()
        if scores:
            context['stars'] = self.get_stars(scores=scores)
        context['items'] = self.get_items()
        return context


class CompanyItemsView(CompanyDetailView):
    template_name = 'reviews/company_items_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.kwargs['item']
        if item in self.item_data:
            item_data = self.item_data[item]
            context['item'] = item
            context['file'] = item_data['file']
            context['name'] = item_data['name']
            item_list = self.object.get_objects(item_data['object'])
            try:
                data = {x: self.get_stars(x.get_scores())
                        for x in item_list}
            except:
                data = {x: {} for x in item_list}
            context['data'] = data

            context['buttons'] = {x: self.item_data[x]['name']
                                  for x in self.item_data.keys() if x != item}
            return context
        else:
            raise Http404


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
        # TODO check here if the website returns 200
        return url


class CompanyCreate(LoginRequiredMixin, CreateView):
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


class CompanyUpdate(LoginRequiredMixin, UpdateView):
    model = Company
    fields = ['name', 'headquarters_city', 'website']
    #template_name = 'reviews/company_view.html'


class CompanyDelete(LoginRequiredMixin, DeleteView):
    model = Company
    success_url = reverse_lazy('home')


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['title', 'position', 'city', 'years_at_company', 'advancement',
                  'worklife', 'compensation', 'environment', 'overallscore',
                  'pros', 'cons', 'comment']

        labels = {
            'title': 'tytuł recenzji',
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
            'advancement': RadioSelectModified(),
            'worklife': RadioSelectModified(),
            'compensation': RadioSelectModified(),
            'environment': RadioSelectModified(),
            'overallscore': RadioSelectModified(),
            'pros': forms.Textarea(),
            'cons': forms.Textarea(),
        }
"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
"""


class ReviewCreate(LoginRequiredMixin, CreateView):
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
        print(RadioSelectModified().get_context(
            'advancement', 1, {'class': 'dupa', 'wrap_label': False}))
        context = super().get_context_data(**kwargs)
        context['company_name'] = get_object_or_404(
            Company, pk=self.kwargs['id'])
        context['radios'] = ['overallscore', 'advancement',
                             'compensation', 'environment', 'worklife']
        return context


class SalaryCreate(LoginRequiredMixin, CreateView):
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
        form.instance.company = get_object_or_404(
            Company, pk=self.kwargs['id'])
        # stub value to be replaced with request.user.something
        form.instance.years_experience = 5
        form.instance.city = form.instance.city.title()
        form.instance.position = form.instance.position.title()
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_name'] = get_object_or_404(
            Company, pk=self.kwargs['id'])
        return context


class InterviewCreate(LoginRequiredMixin, CreateView):
    model = Interview
    fields = [
        'position',
        'department',
        'how_got',
        'difficulty',
        'got_offer',
        'questions',
        'impressions'
    ]

    def form_valid(self, form):
        form.instance.company = get_object_or_404(
            Company, pk=self.kwargs['id'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_name'] = get_object_or_404(
            Company, pk=self.kwargs['id'])
        return context


class CompanyList(LoginRequiredMixin, ListView):
    model = Company
    context_object_name = 'company_list'
