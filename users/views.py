import logging

from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeDoneView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render, resolve_url
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import FormView, TemplateView, UpdateView

from .forms import (
    ActivationEmailSendAgainForm,
    CreateProfileForm_profile,
    CreateProfileForm_user,
    PasswordResetCustomForm,
    UserCreationForm,
)
from .models import Profile, User
from .tokens import account_activation_token

logger = logging.getLogger(__name__)


class NoAuthenticatedUsersMixin:
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().get(request, *args, **kwargs)


class Register(View):
    form_class = UserCreationForm
    template_name = "registration/register.html"
    activation_email_template = "registration/account_activation_email.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.email_confirmed = False
            user.save()
            subject = "Activate your account on pracor.pl"
            message = render_to_string(
                self.activation_email_template,
                {
                    "user": user,
                    "domain": get_current_site(request).domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject, message)
            return redirect("account_activation_sent")
        return render(request, self.template_name, {"form": form})


class AccountActivationSentView(NoAuthenticatedUsersMixin, TemplateView):
    template_name = "registration/account_activation_sent.html"


class AccountActivateView(View):
    redirect_view = "email_confirmed"

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.profile.email_confirmed = True
            user.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            messages.success(request, "E-mail confirmed!")
            return redirect(self.redirect_view)
        return render(request, "registration/account_activation_invalid.html")


class RegisterSuccess(TemplateView):
    template_name = "registration/register_success.html"


class CreateProfileView(LoginRequiredMixin, View):
    user_form_class = CreateProfileForm_user
    profile_form_class = CreateProfileForm_profile
    template_name = "registration/create_profile.html"

    def get(self, request, *args, **kwargs):
        profile_form = self.profile_form_class()
        return render(request, self.template_name, {"profile_form": profile_form})

    def post(self, request, *args, **kwargs):
        profile_form = self.profile_form_class(
            request.POST, instance=request.user.profile
        )
        if profile_form.is_valid():
            profile_form.save()
            return redirect("register_success")
        return render(request, self.template_name, {"profile_form": profile_form})


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    form_class = CreateProfileForm_profile
    template_name = "registration/profile_update_form.html"
    success_url = reverse_lazy("profile")

    def get_context_data(self, **kwargs):
        self.initial = self.request.user.profile.__dict__
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        if self.request.user.has_usable_password():
            context["password"] = True
        return context

    def get_object(self):
        return self.request.user.profile

    def form_valid(self, form):
        messages.success(self.request, "Changes saved.")
        return super().form_valid(form)


class LoginErrorView(NoAuthenticatedUsersMixin, TemplateView):
    template_name = "registration/login_error.html"


class LoginCustomView(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        redirect_to = super().get_success_url()
        if redirect_to == self.request.path or redirect_to == "/logged_out/":
            redirect_to = resolve_url("home")
        return redirect_to

    def form_valid(self, form):
        user = form.get_user()
        if not user.profile.email_confirmed:
            return redirect("email_confirm_reminder")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["self"] = self.request.GET.get("self", "")
        return context


class PasswordResetCustomView(NoAuthenticatedUsersMixin, PasswordResetView):
    form_class = PasswordResetCustomForm
    template_name = "registration/password_reset.html"


class PasswordResetDoneCustomView(NoAuthenticatedUsersMixin, PasswordResetDoneView):
    template_name = "registration/password_done.html"


class PasswordResetConfirmCustomView(
    NoAuthenticatedUsersMixin, PasswordResetConfirmView
):
    template_name = "registration/password_confirm.html"


class PasswordResetCompleteCustomView(PasswordResetCompleteView):
    template_name = "registration/password_complete.html"


class PasswordChangeCustomView(PasswordChangeView):
    template_name = "registration/password_change.html"


class PasswordChangeDoneCustomView(PasswordChangeDoneView):
    template_name = "registration/password_changed.html"


class LoggedOutView(NoAuthenticatedUsersMixin, TemplateView):
    template_name = "registration/loggedout.html"


class EmailConfirmReminderView(NoAuthenticatedUsersMixin, TemplateView):
    template_name = "registration/email_confirm_reminder.html"


class ActivationEmailSendAgain(NoAuthenticatedUsersMixin, FormView):
    form_class = ActivationEmailSendAgainForm
    template_name = "registration/activation_email_send_again.html"
    activation_email_template = "registration/account_activation_email.html"
    success_url = reverse_lazy("account_activation_sent")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return redirect("account_activation_sent")
        subject = "Account Activation on pracor.pl - Resent"
        message = render_to_string(
            self.activation_email_template,
            {
                "user": user,
                "domain": get_current_site(self.request).domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            },
        )
        user.email_user(subject, message)
        return super().form_valid(form)


class SocialAuthErrorView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("profile")
        return redirect("login")


class SocialAuthSetPassword(LoginRequiredMixin, FormView):
    template_name = "registration/set_password.html"
    form_class = SetPasswordForm
    success_url = reverse_lazy("profile")

    def get(self, request, *args, **kwargs):
        if request.user.has_usable_password():
            return redirect("profile")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["user"] = self.request.user
        return context

    def get_form(self):
        return self.form_class(self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")
        messages.success(self.request, "Changes saved.")
        return super().form_valid(form)
