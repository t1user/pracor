from django.conf.urls import url
from .views import ReviewView, CompanysearchView, CompanyDetailView, CompanyCreateView


urlpatterns = [
    #url(r'^review/$', ReviewView.as_view(), name='review'),
    url(r'^review/(?P<id>\d*)/?$',
        ReviewView.as_view(), name='review'),

    #url(r'^search/$', CompanysearchView.as_view(), name='searchcompany'),
    url(r'^search/(?P<searchterm>\w*)/?$',
        CompanysearchView.as_view(), name='searchcompany'),
    url(r'^company/(?P<pk>\d+)/?$',
        CompanyDetailView.as_view(), name='companypage'),
    url(r'^company/create/(?P<company>\w+)/?$',
        CompanyCreateView.as_view(), name='companycreate'),
]
