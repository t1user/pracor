from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django import forms
from django.contrib.auth import (
    login, authenticate, get_user_model, password_validation,)

from django.utils.translation import ugettext, ugettext_lazy as _

from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CreateProfileForm_user, CreateProfileForm_profile
from .models import User


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ("email",)
        field_classes = {'email': forms.EmailField}

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        if self._meta.model.EMAIL_FIELD in self.fields:
            self.fields[self._meta.model.EMAIL_FIELD].widget.attrs.update(
                {'autofocus': True})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        #self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(
            self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class Register(View):
    form_class = UserCreationForm
    template_name = "registration/register.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name,
                      {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('create_profile')

        else:
            return render(request, self.template_name, {'form': form})


class RegisterSuccess(TemplateView):
    template_name = "registration/register_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['session_data'] = self.request.session['linkedin_data']
        return context


    
class CreateProfileView(LoginRequiredMixin, View):
    """
    View with two forms to fill in missing data in User model and Profile.
    Currently not in use because name is not neccessary.
    """
    user_form_class = CreateProfileForm_user
    profile_form_class = CreateProfileForm_profile
    template_name = "reviews/create_profile.html"

    def get(self, request, *args, **kwargs):
        if request.user.last_name == '':
            user_form = self.user_form_class()
        else:
            user_form = {}
        profile_form = self.profile_form_class()
        return render(request, self.template_name,
                      {'user_form': user_form,
                       'profile_form': profile_form})

    def post(self, request, *args, **kwargs):
        user_form = self.user_form_class(request.POST, instance=request.user)
        #profile = Profile.objects.get(user=request.user)
        profile_form = self.profile_form_class(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            #profile = profile_form.save(commit=False)
            #profile.user = request.user
            profile_form.save()
            return redirect('register_success')
        return render(request, self.template_name,
                          {'user_form': user_form,
                           'profile_form': profile_form})
        

class LoginErrorView(View):
    """
    Redirected to if there's a social auth login error and the error is not
    caught by the middleware. Currently happens when debug is off.
    """

    template_name = "registration/login_error.html"

    def get(self, request, *args, **kwargs):
        print(kwargs)
        return render(request,self.template_name)

        
