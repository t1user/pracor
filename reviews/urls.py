from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^$',
        HomeView.as_view(), name='home'),

    url(r'^create_profile',
        CreateProfileView.as_view(), name='create_profile'),

    url(r'^review/(?P<id>\d*)/?$',
        ReviewCreate.as_view(), name='review'),

    url(r'^search/(?P<searchterm>.*)/?$',
        CompanySearchView.as_view(), name='company_search'),

    url(r'^company/(?P<pk>\d+)/(?P<item>\w+)/?$',
        CompanyItemsView.as_view(), name='company_items'),

    url(r'^company/(?P<pk>\d+)/?$',
        CompanyDetailView.as_view(), name='company_page'),

    url(r'^company/create/(?P<company>.*)/?$',
        CompanyCreate.as_view(), name='company_create'),

    url(r'^company/update/(?P<pk>\d+)/?$',
        CompanyUpdate.as_view(), name='company_update'),

    url(r'^company/delete/(?P<pk>\d+)/?$',
        CompanyDelete.as_view(), name='company_delete'),

    url(r'^company/list/?$',
        CompanyList.as_view(), name='company_list'),

    url(r'^salary/(?P<id>\d*)/?$',
        SalaryCreate.as_view(), name='salary'),

    url(r'^interview/(?P<id>\d*)/?$',
        InterviewCreate.as_view(), name='interview'),
]
