from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse, reverse_lazy
from django.views.generic import (UpdateView, DeleteView, CreateView,
                                  ListView, DetailView, TemplateView)
from django.contrib.auth.mixins import (LoginRequiredMixin, PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)

from django.conf import settings

from .models import Company, Salary, Review, Interview, Position
from .forms import (CompanySearchForm, CompanyCreateForm, PositionForm,
                    ReviewForm, SalaryForm, InterviewForm,
                    CompanySelectForm)
from pprint import pprint


class AccessBlocker(UserPassesTestMixin):
    """
    Works with UserPassesTestMixin to block access to certain views for users
    who haven't contributed to the site yet. Redirection site (login_url) 
    should explain what kind of contribution user has to make to get 
    full access.
    """
    login_url = reverse_lazy('please_contribute')
    
    def test_func(self):
        return self.request.user.profile.contributed

class SuperuserAccessBlocker(UserPassesTestMixin):
    """
    Limits access to the view to superusers only.
    """
    raise_exception = True
    
    def test_func(self):
        return self.request.user.is_superuser

class PleaseContributeView(LoginRequiredMixin, TemplateView):
    """
    User redirected to this view if blocked from viewing a view that
    requires contribution. The template should explain what contribution
    is required to get full access.
    """
    
    template_name = 'reviews/please_contribute.html'


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
    #redirects back to itself
    redirect_view = 'company_search'

    def get(self, request, *args, **kwargs):
        """Used to display both:  search form or search results."""
        if request.is_ajax():
            search_results = self.get_results(request.GET.get('term',''))
            options = []
            for item in search_results:
                search_item = {}
                search_item['id'] = item.pk
                search_item['label'] = item.name
                search_item['value'] = item.name
                options.append(search_item)
            print(options)
            return JsonResponse(options, safe=False)
                                         
        
        search_results = ''
        searchterm_joined = kwargs.get('searchterm')
        searchterm = searchterm_joined.replace('_', ' ')
        if searchterm:
            search_results = self.get_results(searchterm)
            #search_results = Company.objects.filter(name__search=searchterm)
            #search_results = Company.objects.filter(name__iregex=r"\y{0}\y".format(searchterm))
            self.template_name = self.redirect_template_name
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name,
                      {'form': form,
                       'search_results': search_results,
                       'searchterm': searchterm,
                       'searchterm_joined': searchterm_joined})

    def get_results(self, searchterm):
        return Company.objects.filter(name__unaccent__icontains=searchterm)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            searchterm = form.cleaned_data['company_name'].replace(' ', '_')
            return HttpResponseRedirect(reverse(self.redirect_view,
                                                kwargs={'searchterm': searchterm}))
        return render(request, self.template_name, {'form': form})


class CompanyDetailView(LoginRequiredMixin, DetailView):
    """
    Displays Company details with last item of each Review, Salary, Interview. 
    Is inherited by CompanyItemsView, which displays lists of all items 
    (Review, Salary, Interview). Company objects are looked up by pk, slug
    is added at the end of url for seo, but is not used for lookup.
    """
    model = Company
    template_name = 'reviews/company_view.html'
    context_object_name = 'company'
    item_data = {'review':
                 {'object': Review,
                  'name': 'opinie',
                  'file': 'reviews/review_item.html',
                  },
                 'salary':
                 {'object': Salary,
                  'name': 'zarobki',
                  'file':  'reviews/salary_item.html',
                  },
                 'interview':
                 {'object': Interview,
                  'name': 'rozmowy',
                  'file':  'reviews/interview_item.html',
                  },
                 }

    def get(self, request, *args, **kwargs):
        """
        Override get() to make sure the view has been called with correct slug.
        If not, redirect.
        """
        self.object = self.get_object()
        # this is required only for CompanyItemsView, which inherits from this one
        item = self.kwargs.get('item', None)
        if self.kwargs.get('slug') != self.object.slug:
            if item is None:
                return redirect(self.object)
            else:
                return redirect('company_items', pk=self.object.pk,
                                slug=self.object.slug, item=item)
        else:
            #this is a copy of superclass, not called by super()
            #to avoid calling self.get_object() again (redundand database call)
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
    
    def get_items(self, **kwargs):
        """
        Items are one last Review, Salary, Interview with 
        accompanying data (template file name, total number of each items, 
        stars, etc). The method is called by get_conext to add the items
        to the context for rendering.
        """
        items = {}
        for key, value in self.item_data.items():
            # reminder: self.object is Company instance
            object = self.object.get_objects(value['object'])
            count = object.count()
            last = object.last()
            try:
                scores = last.get_scores()
                stars = self.get_stars(scores)
            except Exception as e:
                print(e)
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
        """
        Create a dictionary with the number of full, half and blank rating stars for 
        a given dictionary of scores. 
        The dictionary 'scores' has to be in the format:
        {'overallscore': overallscore,
         'advancement': advancement,
         'worklife': worklife,
         'compensation': compensation,
         'environment': environment,} 
        """
        rating_items = {}
        for key, value in scores.items():
            (full, half, blank) = self.count_stars(value)
            # add field names to context to allow for looping over rating
            # items
            try:
                label = self.object._meta.get_field(key).verbose_name
            except:
                #this is for Interview.rating
                label = key
            rating_items[key] = {'rating': value,
                                 'full': full,
                                 'half': half,
                                 'blank': blank,
                                 'label': label}
        return rating_items

    def count_stars(self, value):
        """
        Performs actual stars calculations. Used for Reviews and Interviews.
        """
        truncated = int(value)
        half = value - truncated
        if 0.25 <= half < 0.75:
            half = 1
        else:
            half = 0
        if value - truncated >= 0.75:
            truncated += 1
        # full and blank are iterators to allow for looping in templates
        full = range(truncated)
        blank = range(5 - truncated - half)
        return (full, half, blank)

    
    def get_context_data(self, **kwargs):
        """
        Adds number of stars for Company ratings.
        """
        context = super().get_context_data(**kwargs)
        # get_scores() is a model method
        scores = self.object.get_scores()
        if scores:
            context['stars'] = self.get_stars(scores=scores)
        context['items'] = self.get_items()
        #pprint(context)
        return context


class CompanyItemsView(CompanyDetailView, AccessBlocker):
    """Used to display lists of reviews/salaries/interviews."""
    template_name = 'reviews/company_items_view.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        """"
        Method first determines what item (review/salary/interview) is required 
        and pulls relevant data. Then activates paginator and returns data to context.
        """
        context = super().get_context_data(**kwargs)
        item = self.kwargs['item']

        #translate from Polish word in url to English word used in code
        translation_dict = {'opinie': 'review',
                            'zarobki': 'salary',
                            'rozmowy': 'interview'}
        #if item is a Polish word, translate it, otherwise don't change
        item = translation_dict.get(item, item)

        if item in self.item_data:
            item_data = self.item_data[item]
            context['item'] = item
            context['file'] = item_data['file']
            context['name'] = item_data['name']
            item_list = self.object.get_objects(item_data['object']).order_by('-date')
            if self.paginate_by and (len(item_list) > self.paginate_by):
                context['is_paginated'] = True
                paginator = Paginator(item_list, self.paginate_by)
                page = self.request.GET.get('page')
                try:
                    items = paginator.page(page)
                except PageNotAnInteger:
                    items = paginator.page(1)
                except EmptyPage:
                    items = paginator.page(paginator.num_page)
                item_list = items
                context['page_obj'] = item_list
                context['paginator'] = paginator
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
        # this is typically done in superclass, doing it here gives access to newly created object
        self.object = form.save()
        # this is used if sent here by LinkedInAssociateView
        new_names = self.request.session.get('new_names')
        print(new_names)
        if new_names:
            current_company = self.kwargs.get('company')
            print(current_company)
            for name in new_names:
                if current_company == name[1]:
                    position = Position.objects.get(company_name=current_company)
                    print(self.object)
                    print(self.object.id)
                    position.company = self.object
                    position.save(update_fields=['company'])
                    print(name)
                    new_names.remove(name)
                    print('new names after remove: ', self.request.session['new_names'])
                    self.request.session['new_names'] = new_names
            try:
                new_name = new_names.pop()
                self.success_url = new_name[1]
            except:
                pass
        # calling superclass is unnessesary as all it does is self.object=form.save()
        # (done above) plus the redirect below
        return HttpResponseRedirect(self.get_success_url())


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


class CompanyUpdate(LoginRequiredMixin, SuperuserAccessBlocker, UpdateView):
    model = Company
    fields = ['name', 'headquarters_city', 'website']
    #template_name = 'reviews/company_view.html'


class CompanyDelete(LoginRequiredMixin, SuperuserAccessBlocker, DeleteView):
    model = Company
    success_url = reverse_lazy('home')


class ContentInput(LoginRequiredMixin, View):
    """
    This class is not in use.
    """
    content_form_class = ReviewForm
    position_form_class  = PositionForm
    model = Review
    template_name = "reviews/review_form.html"

    def get(self, request, *args, **kwargs):
        content_form = self.content_form_class()
        position_form = self.position_form_class()
        return render(request, self.template_name,
                      {'content_form': content_form,
                       'position_form': position_form})

    def post(self, request, *args, **kwargs):
        content_form = self.content_form_class(request.POST)
        position_form = self.position_form_class(request.POST)
        if content_form.is_valid() and position_form.is_valid():
            content_form.save()
            position_form.save()
            return redirect('register_success')
        return render(request, self.template_name,
                          {'content_form': content_form,
                           'position_form': position_form})


class ContentCreateAbstract(LoginRequiredMixin, CreateView):
    """
    Creates custom CreateView class to be inherited by views creating
    Reviews and Salaries. On top of standard CreateView functionality
    allows for rendering and processing of an additional form, 
    which creates or recalls correct Position object.
    """
    position_form_class = PositionForm

    def get_context_data(self, **kwargs):
        """
        Adds to context Company object as well as second
        form called 'position_form'.
        """
        context = super().get_context_data(**kwargs)
        self.company = get_object_or_404(Company, pk=self.kwargs['id'])
        context['company'] = self.company
        context['form'].instance.company = self.company
        if 'position_form' not in kwargs and self.two_forms():
            position_form = self.get_position_form()
            position_form.instance.company = self.company
            context['position_form'] = position_form
        return context

    def get_position_instance(self):
        """
        If user has a position associated with the Company
        they're trying to review, this instance should be 
        associated with the review.
        """
        try:
            position_instance = Position.objects.filter(company=self.company,
                                                        user=self.request.user)
            return position_instance[0]
        except:
            return None

    def two_forms(self):
        if self.get_position_instance():
            return False
        else:
            return True
        
    def get_position_form(self):
        """
        Return an instance of position_form. Method mirrors
        standard get_form().
        """
        return self.position_form_class(**self.get_form_kwargs())
    
    def post(self, request, *args, **kwargs):
        """
        Handles POST request, instantiating two forms with passed POST
        data and  validating it. is_valid and is_invalid methods 
        have been overriden to handle two forms instead 
        of one. two_forms returns True if the second form is required.
        """
        self.company = get_object_or_404(Company, pk=self.kwargs['id'])
        form = self.get_form()
        if self.two_forms():
            position_form = self.get_position_form()
            if form.is_valid() and position_form.is_valid():
                return self.form_valid(form=form,
                                       position_form=position_form)
            else:
                return self.form_invalid(form=form,
                                         position_form=position_form)
        else:
            return self.form_valid(form=form)
            
    def form_valid(self, form, **kwargs):
        """
        Extends the standard method to save position_form. 
        """
 
        form.instance.user = self.request.user
        form.instance.company = self.company
        if self.two_forms():
            position_form = kwargs['position_form']
            position_form.instance.user = self.request.user
            position_form.instance.company = self.company
            position = position_form.save()
            form.instance.position = position
        else:
            form.instance.position = self.get_position_instance()
        #last two items are direct quotes from super(),
        #broght here only for more explicity
        self.object = form.save()
        # give user full access to views that require contribution to the site
        self.request.user.profile.contributed = True
        self.request.user.profile.save(update_fields = ['contributed'])
        return HttpResponseRedirect(self.get_success_url())
            
    def form_invalid(self, form, position_form):
        """
        Override to enable for handling of two forms. If only one form,
        superclass used.
        """
        if self.two_forms():
            return self.render_to_response(self.get_context_data(form=form,
                                            position_form=position_form))
        else:
            return super().form_valid(form)



class ReviewCreate(ContentCreateAbstract):
    form_class = ReviewForm
    template_name = "reviews/review_form.html"
    
class SalaryCreate(ContentCreateAbstract):
    form_class = SalaryForm
    template_name = "reviews/salary_form.html"
    
class ReviewCreateOld(LoginRequiredMixin, CreateView):
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
        #form.instance.position = form.instance.position.title()
        #form.instance.city = form.instance.city.title()
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_name'] = get_object_or_404(
            Company, pk=self.kwargs['id'])
        #context['radios'] = ['overallscore', 'advancement',
        #                     'compensation', 'environment', 'worklife']
        return context


class SalaryCreateOld(LoginRequiredMixin, CreateView):
    form_class = SalaryForm
    model = Salary

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
    form_class = InterviewForm
    model = Interview

    def form_valid(self, form):
        form.instance.company = get_object_or_404(
            Company, pk=self.kwargs['id'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_name'] = get_object_or_404(
            Company, pk=self.kwargs['id'])
        return context


class CompanyList(LoginRequiredMixin, SuperuserAccessBlocker, ListView):
    model = Company
    context_object_name = 'company_list'
    paginate_by = 20

                
class LinkedinCreateProfile(LoginRequiredMixin, View):
    """
    Presents forms to a user logged in with linkedin so that they can 
    associate their linkedin position with a Company from the database.
    """
    form_class = CompanySelectForm
    template_name = "reviews/linkedin_associate.html"
    
    def get(self, request, *args, **kwargs):
        # we are redirected here by social_pipeline_override.py
        # session should have unassociated company names
        # companies is a list of tuples of (position.id, company_name)
        companies = request.session['companies']
        names = [name[1] for name in companies]
        print('from session: ', companies)
        candidates = {}
        new_names = []
        for company in companies:
            print('iteration: ', company)
            company_db = Company.objects.filter(name__icontains=company[1])
            if company_db.count() > 0:
                # candidates are companies that have database entries similar
                # to their names, user is suggested to chose an association
                # candidates[company_name] = (position_id, company_name, company_db)
                candidates[company[1]] = (company[0], company[1], company_db) 
            else:
                # new names are names that haven't been found in the database
                # so potentially they have to be appended, user will be given 
                # an option to get redirected to a form creating new company
                new_names.append(company)
                pass
        request.session['new_names'] = new_names
        forms = {}
        if candidates:
            print(candidates)
            form_choices = {}
            # company_tuple is a tuple of (position_id, company_name, company_db)
            for candidate, company_tuple in candidates.items():
                # will be used as choices parameter on the form
                choices = [(company.pk, company.name) for company in company_tuple[2]]
                print('candidate: ', candidate)
                print('options: ', companies)
                forms[candidate] = self.form_class(companies=choices,
                                                   prefix=candidate,
                                                   initial={'position': company_tuple[0]})
                form_choices[candidate] = choices
            request.session['form_choices'] = form_choices
        #else:
            #request.session['new_names'] = new_names
        print('companies: ', companies, 'candidates: ', candidates, 'new_names: ', new_names, 'forms: ', forms)
        return render(request, self.template_name,
                      {'companies': names,
                       'candidates': candidates,
                       'new_names': new_names,
                       'forms': forms})

    def post(self, request, *args, **kwargs):
        form_choices = request.session['form_choices']
        forms = {}
        valid = True
        for candidate, choices in form_choices.items():
            form = self.form_class(request.POST,
                                   companies=choices,
                                   prefix=candidate)
            if not form.is_valid():
                valid = False
            forms[candidate] = form
        if valid:
            new_names = []
            for name, form in forms.items():
                company_pk = form.cleaned_data.get('company_name')
                if company_pk == 'None':
                    company_pk = None
                position_pk = form.cleaned_data.get('position')
                position = Position.objects.get(pk=position_pk)
                print(company_pk is None)
                if company_pk:
                    print('I am inside')
                    company = Company.objects.get(pk=company_pk)
                    position.company = company
                    position.save(update_fields=['company'])
                else:
                    new_names.append((position.id, name))
 
            
            if request.session.get('new_names') or new_names:
                request.session['new_names'] += new_names

            print('new_names: ', request.session.get('new_names'))                
            if request.session['new_names']:
                index = len(request.session['new_names']) - 1
                return redirect('company_create', company=request.session['new_names'][index][1])
            else:
                return redirect('home')
        else:
            print(forms)
            return render(request, self.template_name,
                          {'forms': forms})
    
        
