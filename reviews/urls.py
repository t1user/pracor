from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^$',
        HomeView.as_view(), name='home'),

    url(r'^please_contribute/$',
        PleaseContributeView.as_view(), name='please_contribute'),

    url(r'^linkedin_associate',
        LinkedinCreateProfile.as_view(), name='linkedin_associate'),

    url(r'^review/(?P<id>\d*)/$',
        ReviewCreate.as_view(), name='review'),

    url(r'^search/(?P<searchterm>.*)/$',
        CompanySearchView.as_view(), name='company_search'),

    url(r'^(?P<pk>\d+)/(?P<item>\w+)/(?P<slug>[-\w\d]+)?$',
        CompanyItemsView.as_view(), name='company_items'),

    url(r'^(?P<pk>\d+)/(?P<slug>[-\w\d]+)?$',
        CompanyDetailView.as_view(), name='company_page'),

    url(r'^company/create/(?P<company>.*)/$',
        CompanyCreate.as_view(), name='company_create'),

    url(r'^company/update/(?P<pk>\d+)/$',
        CompanyUpdate.as_view(), name='company_update'),

    url(r'^company/delete/(?P<pk>\d+)/$',
        CompanyDelete.as_view(), name='company_delete'),

    url(r'^company/list/$',
        CompanyList.as_view(), name='company_list'),

    url(r'^salary/(?P<id>\d*)/$',
        SalaryCreate.as_view(), name='salary'),

    url(r'^interview/(?P<id>\d*)/$',
        InterviewCreate.as_view(), name='interview'),
]
