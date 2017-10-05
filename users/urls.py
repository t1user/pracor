from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^create_profile',
        CreateProfileView.as_view(), name='create_profile'),

    url(r'^register/', Register.as_view(), name='register'),
    
    url(r'^register_success/', RegisterSuccess.as_view(), name='register_success'),
]


