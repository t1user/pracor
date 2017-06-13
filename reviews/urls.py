from django.conf.urls import url
from .views import ReviewView, CompanysearchView

urlpatterns = [
    url(r'^review$', ReviewView.as_view(), name='review' ),
    url(r'^search$', CompanysearchView.as_view(), name='searchcompany'),
    ]


