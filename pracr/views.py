from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    data = request.META
    return render(request, 'home.html', {'data': data})

def profile(request):
    print('USER: ', request.user)
    social_user = request.user.social_auth.get(provider='linkedin-oauth2')
    data = social_user.extra_data
    return render(request, 'profile.html', {'data': data})



