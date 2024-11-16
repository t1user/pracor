from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path(
        "please_contribute/",
        views.PleaseContributeView.as_view(),
        name="please_contribute",
    ),
    path(
        "email_confirmed/", views.EmailConfirmedView.as_view(), name="email_confirmed"
    ),
    path(
        "linkedin_associate",
        views.LinkedinCreateProfile.as_view(),
        name="linkedin_associate",
    ),
    re_path(
        r"^search_add/(?P<item>\w+)/(?P<searchterm>.*)?$",
        views.CreateItemSearchView.as_view(),
        name="create_item_search",
    ),
    re_path(
        r"^search/(?P<searchterm>.*)?$",
        views.CompanySearchView.as_view(),
        name="company_search",
    ),
    re_path(
        r"^(?P<pk>\d+)/opinie/(?P<slug>[-\w\d]+)?$",
        views.ReviewItemsView.as_view(),
        name="review_items",
    ),
    re_path(
        r"^(?P<pk>\d+)/zarobki/(?P<slug>[-\w\d]+)?$",
        views.SalaryItemsView.as_view(),
        name="salary_items",
    ),
    re_path(
        r"^(?P<pk>\d+)/rozmowy/(?P<slug>[-\w\d]+)?$",
        views.InterviewItemsView.as_view(),
        name="interview_items",
    ),
    re_path(
        r"^(?P<pk>\d+)/(?P<item>\w+)/(?P<slug>[-\w\d]+)?$",
        views.CompanyItemsRedirectView.as_view(),
        name="company_items",
    ),
    re_path(
        r"^(?P<pk>\d+)/(?P<slug>[-\w\d]+)?$",
        views.CompanyDetailView.as_view(),
        name="company_page",
    ),
    re_path(
        r"^search_company/create/(?P<item>\w+)/(?P<company>.*)/$",
        views.SearchCompanyCreate.as_view(),
        name="search_company_create",
    ),
    re_path(
        r"^company/create/(?P<company>.*)/$",
        views.CompanyCreate.as_view(),
        name="company_create",
    ),
    re_path(
        r"^company/update/(?P<pk>\d+)/$",
        views.CompanyUpdate.as_view(),
        name="company_update",
    ),
    re_path(
        r"^company/delete/(?P<pk>\d+)/$",
        views.CompanyDelete.as_view(),
        name="company_delete",
    ),
    path("company/list/", views.CompanyList.as_view(), name="company_list"),
    re_path(
        r"^dodaj/opinie/(?P<id>\d*)/(?P<slug>[-\w\d]+)?/$",
        views.ReviewCreate.as_view(),
        name="review",
    ),
    re_path(
        r"^dodaj/zarobki/(?P<id>\d*)/(?P<slug>[-\w\d]+)?/$",
        views.SalaryCreate.as_view(),
        name="salary",
    ),
    re_path(
        r"^dodaj/rozmowy/(?P<id>\d*)/(?P<slug>[-\w\d]+)?/$",
        views.InterviewCreate.as_view(),
        name="interview",
    ),
    path("kontakt/", views.ContactView.as_view(), name="contact"),
]
