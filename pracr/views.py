from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.views.generic import TemplateView


def home(request):
    data = request.META
    return render(request, 'home.html', {'data': data})


def profile(request):
    print('USER: ', request.user)
    social_user = request.user.social_auth.get(provider='linkedin-oauth2')
    data = social_user.extra_data
    return render(request, 'profile.html', {'data': data})


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
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('register_success')

        else:
            form = UserCreationForm()

        return render(request, 'signup.html', {'form': form})


class RegisterSuccess(TemplateView):
    template_name = "registration/register_success"
