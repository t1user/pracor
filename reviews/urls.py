from django.conf.urls import url
from .views import ReviewView, CompanysearchView, companyview, CompanyDetailView


urlpatterns = [
    url(r'^review/$', ReviewView.as_view(), name='review'),
    #url(r'^search/$', CompanysearchView.as_view(), name='searchcompany'),
    url(r'^search/(?P<searchterm>\w*)/?$',
        CompanysearchView.as_view(), name='searchcompany'),
    url(r'^company/(?P<pk>\d+)/?$',
        CompanyDetailView.as_view(), name='companypage'),
]
