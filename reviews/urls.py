from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$',
        HomeView.as_view(), name='home'),

    url(r'^please_contribute/$',
        PleaseContributeView.as_view(), name='please_contribute'),

    url(r'^email_confirmed/$',
        EmailConfirmedView.as_view(), name='email_confirmed'),

    url(r'^linkedin_associate',
        LinkedinCreateProfile.as_view(), name='linkedin_associate'),

    url(r'^search_add/(?P<item>\w+)/(?P<searchterm>.*)?$',
        CreateItemSearchView.as_view(), name='create_item_search'),

    url(r'^search/(?P<searchterm>.*)?$',
        CompanySearchView.as_view(), name='company_search'),

    url(r'^(?P<pk>\d+)/opinie/(?P<slug>[-\w\d]+)?$',
        ReviewItemsView.as_view(), name='review_items'),

    url(r'^(?P<pk>\d+)/zarobki/(?P<slug>[-\w\d]+)?$',
        SalaryItemsView.as_view(), name='salary_items'),

    url(r'^(?P<pk>\d+)/rozmowy/(?P<slug>[-\w\d]+)?$',
        InterviewItemsView.as_view(), name='interview_items'),
    
    url(r'^(?P<pk>\d+)/(?P<item>\w+)/(?P<slug>[-\w\d]+)?$',
        CompanyItemsRedirectView.as_view(), name='company_items'),

    url(r'^(?P<pk>\d+)/(?P<slug>[-\w\d]+)?$',
        CompanyDetailView.as_view(), name='company_page'),

    url(r'search_company/create/(?P<item>\w+)/(?P<company>.*)/$',
        SearchCompanyCreate.as_view(), name='search_company_create'),
    
    url(r'^company/create/(?P<company>.*)/$',
        CompanyCreate.as_view(), name='company_create'),

    url(r'^company/update/(?P<pk>\d+)/$',
        CompanyUpdate.as_view(), name='company_update'),

    url(r'^company/delete/(?P<pk>\d+)/$',
        CompanyDelete.as_view(), name='company_delete'),

    url(r'^company/list/$',
        CompanyList.as_view(), name='company_list'),

    url(r'^dodaj/opinie/(?P<id>\d*)/(?P<slug>[-\w\d]+)?/$',
        ReviewCreate.as_view(), name='review'),

    url(r'^dodaj/zarobki/(?P<id>\d*)/(?P<slug>[-\w\d]+)?/$',
        SalaryCreate.as_view(), name='salary'),

    url(r'^dodaj/rozmowy/(?P<id>\d*)/(?P<slug>[-\w\d]+)?/$',
        InterviewCreate.as_view(), name='interview'),

    url(r'^kontakt/$', ContactView.as_view(), name='contact')
]
