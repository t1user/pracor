from django.conf.urls import url
from .views import *
#from .views import ReviewView, CompanySearchView, CompanyDetailView, CompanyCreateView


urlpatterns = [
    url(r'^review/(?P<id>\d*)/?$',
        ReviewView.as_view(), name='review'),

    url(r'^search/(?P<searchterm>.*)/?$',
        CompanySearchView.as_view(), name='company_search'),

    url(r'^company/(?P<pk>\d+)/?$',
        CompanyDetailView.as_view(), name='company_page'),

    url(r'^company/create/(?P<company>.*)/?$',
        CompanyCreateView.as_view(), name='company_create'),

    url(r'^company/update/(?P<pk>\d+)/?$',
        CompanyUpdate.as_view(), name='company_update'),

    url(r'^company/delete/(?P<pk>\d+)/?$',
        CompanyDelete.as_view(), name='company_delete'),

    url(r'^salary/(?P<id>\d*)/?$',
        SalaryCreate.as_view(), name='salary'),
]
