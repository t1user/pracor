
from .forms import (CompanySearchForm, ReviewForm, SalaryForm,
                    CompanyForm)


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

