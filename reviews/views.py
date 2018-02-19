import hashlib
import datetime
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy, resolve
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView, RedirectView, FormView)
from django.views.generic.detail import SingleObjectMixin
from django.db.models import Q
from django.utils import timezone
from django import forms


from users.models import Visit

from .forms import (CompanyCreateForm, CompanySearchForm, CompanySelectForm,
                    InterviewForm, PositionForm, ReviewForm, SalaryForm, ContactForm)
from .models import Company, Interview, Position, Review, Salary


logger = logging.getLogger(__name__)

def success_message(request):
    """
    Used to display flash message after succesful submission of a form.
    """
    messages.add_message(request, messages.SUCCESS, 'Zapisano dane. Dzięki!')

def failure_message(request, item, days):
    """
    Used to display flash message informing that user cannot submit data.
    """
    messages.add_message(request, messages.WARNING,
                         'Już mamy Twoje dane! {} dla tej firmy możesz ponownie dodać za {} dni.'.format(item, days))
    
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


class AjaxViewMixin:
    """
    Return json data to forms, which use jQuery UI autocomplete widget.
    Views that inherit must imiplement get_results method,
    which returns data to be presented in the form.
    """

    def get(self, request, *args, **kwargs):
        """
        Request json data if request is ajax. Otherwise use super() to handle view.
        """
        if request.is_ajax():
            field = request.GET.get('field', 'id_').replace('id_', '')
            results = self.get_results(
                request.GET.get('term', ''), field
            ).values()
            if field:
                results = results.values(field).distinct()
            if not field:
                field = "name"
            options = []
            for item in results:
                item = {'id': item.get('id'),
                        'label': item.get(field),
                        'value': item.get(field),
                        'slug': item.get('slug')}
                options.append(item)
            return JsonResponse(options, safe=False)
        else:
            return super().get(request, *args, **kwargs)


class CompanySearchBase(View):
    form_class = CompanySearchForm
    initial = {}
    template_name = 'reviews/home.html'
    redirect_template_name = 'reviews/company_search_results.html'
    # after search, redirect back to itself to present results
    redirect_view = 'company_search'

    def get(self, request, *args, **kwargs):
        """Used to display both:  search form or search results."""
        search_results = ''
        searchterm_joined = kwargs.get('searchterm')
        searchterm = searchterm_joined.replace('_', ' ')
        if searchterm:
            search_results = self.get_results(searchterm)
            self.template_name = self.redirect_template_name
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name,
                      {'form': form,
                       'search_results': search_results,
                       'searchterm': searchterm,
                       'searchterm_joined': searchterm_joined})

    def get_results(self, searchterm, *args, **kwargs):
        """Fire database query and returns matching Company objects."""
        return Company.objects.filter(Q(name__unaccent__icontains=searchterm) |
                                      Q(website__unaccent__icontains=searchterm))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            searchterm = form.cleaned_data['company_name'].replace(' ', '_')
            return HttpResponseRedirect(reverse(self.redirect_view,
                                                kwargs={'searchterm': searchterm}))
        return render(request, self.template_name, {'form': form})


class CompanySearchView(AjaxViewMixin, CompanySearchBase):
    """
    Handles searchbar including ajax calls for jQuery UI autocomplete.
    """
    pass


class NoSlugRedirectMixin:
    """
    If view called by GET without a slug, redirect to url with slug. Otherwise, ignore.
    Must be inherited by a CBV with get, which: 1. sets self.object 2. returns self.no_slug().
    """

    def no_slug(self, request, *args, **kwargs):
        """
        Check if view has been called with proper slug, if not redirect.
        """
        if kwargs.pop('slug') != self.object.slug:
            #preserve GET parameters if any
            args = request.META.get('QUERY_STRING', '')
            if args:
                args = '?{}'.format(args)
            url = reverse(resolve(request.path_info).url_name,
                          kwargs={'slug': self.object.slug, **kwargs}) + args
            return redirect(url)
        else:
            return super().get(request, *args, **kwargs)


class CompanyDetailView(LoginRequiredMixin, NoSlugRedirectMixin, DetailView):
    """
    Display Company details with last item of each Review, Salary, Interview.
    The class ss inherited by CompanyItemsView, which displays lists of all items
    (Review, Salary, Interview). Company objects are looked up by pk, slug
    is added at the end of url for seo, but is not used for lookup.
    """
    model = Company
    template_name = 'reviews/company_view.html'
    context_object_name = 'company'

    def get(self, request, *args, **kwargs):
        """
        Required to implement NoSlugRedirectMixin.
        """
        self.object = self.get_object()
        return self.no_slug(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """
        Record visit and
        add items that will  help looping in templates.
        """
        self.record_visit()
        context = super().get_context_data(**kwargs)
        context['items'] = {
            'review': self.object.reviews,
            'salary': self.object.salaries,
            'interview': self.object.interviews,
        }
        return context

    def record_visit(self):
        """
        Record user who visited the Company (date
        of the visit added by model).
        """
        path = self.request.get_full_path()
        ip = self.request.META.get('REMOTE_ADDR')
        if not ip:
            ip = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if not ip:
            ip = self.request.META.get('HTTP_X_REAL_IP')
        Visit.objects.create(company=self.object,
                             user=self.request.user.profile,
                             path=path,
                             ip=ip)


class CompanyItemsRedirectView(RedirectView):
    """A helper function to facilitate accessing xxx_items from templates."""
    pass


class CompanyItemsAbstract(LoginRequiredMixin, AccessBlocker, NoSlugRedirectMixin,
                           SingleObjectMixin,  ListView):
    """
    Abstract base class for displaying lists of Review, Salary, Interview.
    Combines functionality of ListView - list of given items and
    DetailView - Company. 
    This is almost exact copy from Django documentation section on using view mixins.
    """
    
    template_name = 'reviews/company_items_view.html'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        """
        Provide Company object for SingleObjectMixin. Redirect if called
        without slug (implemented by NoSlugRedirectMixin).
        """
        self.object = self.get_object(queryset=Company.objects.all())
        return self.no_slug(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['buttons'] = [x._meta.verbose_name_plural.lower()
                              for x in [Review, Salary, Interview]
                              if x != self.model]
        context['name'] = self.model._meta.verbose_name_plural
        context['model'] = self.model._meta.model_name
        return context

    def get_queryset(self):
        dictionary = {Review: self.object.reviews,
                      Salary: self.object.salaries,
                      Interview: self.object.interviews, }

        return dictionary[self.model]

   
class ReviewItemsView(CompanyItemsAbstract):
    """Display list of reviews for a given Company."""
    model = Review


class SalaryItemsView(CompanyItemsAbstract):
    """Display list of salaries for a given Company."""
    model = Salary


class InterviewItemsView(CompanyItemsAbstract):
    """Display list of interviews for a given Company."""
    model = Interview


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
        # this is typically done in superclass, doing it here gives access to
        # newly created object
        self.object = form.save()
        # this is used if sent here by LinkedInAssociateView
        new_names = self.request.session.get('new_names')
        if new_names:
            current_company = self.kwargs.get('company')
            for name in new_names:
                if current_company == name[1]:
                    position = Position.objects.get(
                        company_name=current_company)
                    position.company = self.object
                    position.save(update_fields=['company'])
                    new_names.remove(name)
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
    # template_name = 'reviews/company_view.html'


class CompanyDelete(LoginRequiredMixin, SuperuserAccessBlocker, DeleteView):
    model = Company
    success_url = reverse_lazy('home')


class TokenVerifyMixin:
    """
    Prevent resubmission of the same form. After saving form data, store
    hashed csrf in session. On form submission check its csrf against the one
    stored in session.
    """

    def post(self, request, *args, **kwargs):
        """
        Check for resubmission of the same form.
        """
        if self.check_token():
            self.company = get_object_or_404(Company, pk=self.kwargs['id'])
            return redirect(self.company)
        return super().post(request, *args, **kwargs)

    def hash_token(self):
        """
        Get csrf token and hash it. 
        Hashing is probably unnessesary, but what the hell...
        """
        token = self.request.POST.get('csrfmiddlewaretoken')
        hash = hashlib.sha1(token.encode('utf-8')).hexdigest()
        return hash

    def save_token(self):
        """
        Store hashed csrf token in session, so that track can be kept on which
        forms have already been saved to database. Allows for prevention of
        multiple submissions of the same form.
        """
        self.request.session['token'] = self.hash_token()

    def check_token(self):
        """
        Compare csrf token with the one stored in session.
        """
        token = self.hash_token()
        stored_token = self.request.session.get('token')
        if token == stored_token:
            return True

    def form_valid(self, *args, **kwargs):
        """
        Store hashed csrf token in session.
        """
        self.save_token()
        return super().form_valid(*args, **kwargs)


class ContentCreateAbstract(LoginRequiredMixin, AjaxViewMixin, CreateView):
    """
    Custom CreateView class to be inherited by views creating
    Reviews and Salaries. On top of standard CreateView functionality
    allows for rendering and processing of an additional form,
    which creates or recalls correct Position object.
    """
    position_form_class = PositionForm

    def get_results(self, searchterm, field):
        """
        Return results for jQuery autocomplete. Used by AjaxViewMixin.
        """
        field = field + '__unaccent__icontains'
        results = Position.objects.filter(
            company=self.kwargs['id'],
            **{field: searchterm},
        )
        return results


    def get_context_data(self, **kwargs):
        """
        Add  Company object to context as well as second
        form called 'position_form'.
        """
        context = super().get_context_data(**kwargs)
        context['company'] = self.company
        context['form'].instance.company = self.company
        if 'position_form' not in kwargs and self.two_forms():
            position_form = self.get_position_form()
            position_form.instance.company = self.company
            context['position_form'] = position_form
        return context

    def get_position_instance(self):
        """
        If user has a position associated with the Company they're trying to review,
        this Position instance should be associated with the review.
        """
        position_instance = Position.objects.filter(company=self.company,
                                                    user=self.request.user)
        if position_instance:
            return position_instance[position_instance.count() - 1]

    def test_position(self):
        """
        Test if there exists a valid (less than 90 days old) item (Salary or Review) 
        for the existing position.
        """
        if self.position:
            #get the position and check how old it is
            item = self.form_class.Meta.model.objects.filter(position=self.position)
            if item:
                item=item[0]
                days = timezone.now() - item.date - datetime.timedelta(days=90)
                if days.days < 0:
                    self.days_until_next = -days.days
                    return False
        return True
                
    def two_forms(self):
        """
        Show two forms, ie. let user create another Position instance, if:
        - they don't have a position for this Company
        - they have a position but haven't submitted this type of item (salary, review)
        - they have a position, submitted item, but this item is more than 90days old
        """
        if self.position:
            if self.test_position:
                return True
            return False
        else:
            return True

    def get_position_form(self):
        """
        Return an instance of position_form. Method mirrors
        standard get_form().
        """
        return self.position_form_class(**self.get_form_kwargs())

    def get(self, request, *args, **kwargs):
        """
        Check if user is allowed to post this content, ie there should
        be only one Salary or Review for every Position.
        """
        self.company = get_object_or_404(Company, pk=self.kwargs['id'])
        self.position = self.get_position_instance()
        #if a content item (salary or review) already exists for this position
        #and its newer than 90 days don't allow to proceed
        if self.position and not self.test_position():
            failure_message(self.request,
                            self.form_class.Meta.model._meta.verbose_name_plural,
                            self.days_until_next)
            return redirect(self.company)
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        """
        Instantiate two forms with passed POST data and validate them.
        is_valid and is_invalid methods have been overriden to handle two forms.
        """
        self.object = None
        self.company = get_object_or_404(Company, pk=self.kwargs['id'])
        self.position = self.get_position_instance()
        form = self.get_form()
        # returns True if the second form is required.
        if self.two_forms():
            position_form = self.get_position_form()
            if form.is_valid() and position_form.is_valid():
                return self.form_valid(form=form,
                                       position_form=position_form)
            else:
                return self.form_invalid(form=form,
                                         position_form=position_form)
        else:
            if form.is_valid():
                return self.form_valid(form=form)
            else:
                return self.form_invalid(form=form)

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
        # last two items are direct quotes from super(),
        # broght here only for more explicity
        self.object = form.save()
        # give user full access to views that require contribution to the site
        self.request.user.profile.contributed = True
        self.request.user.profile.save(update_fields=['contributed'])
        success_message(self.request)
        return redirect(self.get_success_url())

    def form_invalid(self, form, **kwargs):
        """
        Handle two forms. If only one form profided, use superclass.
        """
        if self.two_forms():
            position_form = kwargs['position_form']
            return self.render_to_response(self.get_context_data(form=form,
                                                                 position_form=position_form))
        else:
            return super().form_invalid(form, **kwargs)


class ReviewCreate(TokenVerifyMixin, ContentCreateAbstract):
    form_class = ReviewForm
    template_name = "reviews/review_form.html"


class SalaryCreate(TokenVerifyMixin, ContentCreateAbstract):
    form_class = SalaryForm
    template_name = "reviews/salary_form.html"

    def get_form_kwargs(self):
        """
        Form needs request, because it adds user as author of new benefits.
        Same for Company.
        """
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'request': self.request,
            'company': self.company,
            })
        return kwargs

class InterviewCreate(LoginRequiredMixin, TokenVerifyMixin, CreateView):
    form_class = InterviewForm
    model = Interview

    def get(self, request, *args, **kwargs):
        """
        Check if user is allowed to post, ie. has not posted Interview
        for this Company in the last 90 days.
        """
        company = get_object_or_404(Company, pk=self.kwargs['id'])
        item = Interview.objects.filter(company=company,
                                        user=request.user)
        if item:
            item=item[0]
            days = timezone.now() - item.date - datetime.timedelta(days=90)
            if days.days < 0:
                days_until_next = -days.days
                failure_message(self.request, 'Raport z rozmowy',
                                days_until_next)
                return redirect(company)
        return super().get(request, *args, **kwargs)
        
    def form_valid(self, form):
        form.instance.company = get_object_or_404(
            Company, pk=self.kwargs['id'])
        form.instance.user = self.request.user
        success_message(self.request)
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
        candidates = {}
        new_names = []
        for company in companies:
            company_db = CompanySearchBase.get_results(self, company[1])
            # company_db = Company.objects.filter(name__icontains=company[1])
            if company_db.count() > 0:
                # candidates are companies that have database entries similar
                # to their names, user is suggested to chose an association
                # candidates[company_name] = (position_id, company_name,
                # company_db)
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
            form_choices = {}
            for candidate, company_tuple in candidates.items():
                # will be used as choices parameter on the form
                choices = [(company.pk, company.name)
                           for company in company_tuple[2]]
                forms[candidate] = self.form_class(companies=choices,
                                                   prefix=candidate,
                                                   initial={'position': company_tuple[0]})
                form_choices[candidate] = choices
            request.session['form_choices'] = form_choices
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
                if company_pk:
                    company = Company.objects.get(pk=company_pk)
                    position.company = company
                    position.save(update_fields=['company'])
                else:
                    new_names.append((position.id, name))

            if request.session.get('new_names') or new_names:
                request.session['new_names'] += new_names

            if request.session['new_names']:
                index = len(request.session['new_names']) - 1
                return redirect('company_create', company=request.session['new_names'][index][1])
            else:
                return redirect('home')
        else:
            return render(request, self.template_name,
                          {'forms': forms})


class ContactView(FormView):
    """
    Display form that allows user to send a pre-formatted email to admins. If user is 
    logged-in, don't allow to edit 'from' field. To provide robo-spamming limit number 
    of sent messages to three per day.
    """
    form_class = ContactForm
    success_url = '/'
    template_name = 'reviews/contact.html'


    def form_valid(self, form):
        """
        Send user message to admins.
        """
        sender = form.cleaned_data['your_email']
        if self.request.user.is_authenticated:
            #override to make sure the readonly form field hasn't been tampered with
            sender = self.request.user.email
        subject = '[pracor kontakt] {}'.format(form.cleaned_data['subject'])
        message = 'Wiadomość od: {} \n\n{}'.format(sender,
                                                   form.cleaned_data['message'])
        try:
            send_mail(
                subject,
                message,
                'kontakt@pracor.pl',
                settings.CONTACT_EMAILS,
                fail_silently=False)
            messages.add_message(self.request, messages.SUCCESS, 'Wiadomość została wysłana.')
            self.record_send()
        except:
            messages.add_message(self.request, messages.WARNING, 'Wystąpił błąd, spróbuj ponownie.')
            return redirect('contact')
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        """
        Don't proceed before checking if the user can send message.
        """
        if self.check_if_can_send():
            return super().get(request, *args, **kwargs)
        return redirect(self.get_success_url())
    
    def get_success_url(self, *args, **kwargs):
        """
        Go back to where you came from.
        """
        return self.request.GET.get('next', reverse('home'))
    
    def get_context_data(self, **kwargs):
        #required to prevent user leakage after logout
        self.initial = {}
        if self.request.user.is_authenticated:
            self.initial.update({'your_email': self.request.user.email})
            context = super().get_context_data(**kwargs)
            context['form'].fields['your_email'].widget.attrs['readonly']=True
            return context
        return super().get_context_data(**kwargs)

    def record_send(self):
        no_messages = self.request.session.get('sent_emails', 0)
        no_messages += 1
        self.request.session['sent_emails'] = no_messages
        

    def check_if_can_send(self):
        if self.request.session.get('sent_emails', 0) > 2:
            messages.add_message(self.request, messages.INFO,
                                 'Dostaliśmy już 3 Twoje wiadomości. Daj nam je przeczytać -:)')
            return False
        return True
        
        
