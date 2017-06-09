from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

def profile(request):
    print('USER: ', request.user)
    social_user = request.user.social_auth.get(provider='linkedin-oauth2')
    data = social_user.extra_data
    for key, value in data.items():
        print(key, ': ', value)
    print(type(data))
    return render(request, 'profile.html', {'data': data})



