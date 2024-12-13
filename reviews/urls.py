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
    path("opinie/<pk>/<slug>", views.ReviewItemsView.as_view(), name="review_items"),
    path("zarobki/<pk>/<slug>", views.SalaryItemsView.as_view(), name="salary_items"),
    path(
        "rozmowy/<pk>/<slug>",
        views.InterviewItemsView.as_view(),
        name="interview_items",
    ),
    path(
        "<item>/<pk>/<slug>",
        views.CompanyItemsRedirectView.as_view(),
        name="company_items",
    ),
    path("<pk>/<slug>/", views.CompanyDetailView.as_view(), name="company_page"),
    path("<pk>/", views.CompanyDetailView.as_view(), name="company_page"),
    path(
        "search_company/create/<item>/<company>/",
        views.SearchCompanyCreate.as_view(),
        name="search_company_create",
    ),
    path(
        "company/create/<company>/",
        views.CompanyCreate.as_view(),
        name="company_create",
    ),
    path("company/update/<pk>/", views.CompanyUpdate.as_view(), name="company_update"),
    path("company/delete/<pk>/", views.CompanyDelete.as_view(), name="company_delete"),
    path("company/list/", views.CompanyList.as_view(), name="company_list"),
    path("dodaj/opinie/<id>/<slug>/", views.ReviewCreate.as_view(), name="review"),
    path("dodaj/zarobki/<id>/<slug>/", views.SalaryCreate.as_view(), name="salary"),
    path(
        "dodaj/rozmowy/<id>/<slug>/", views.InterviewCreate.as_view(), name="interview"
    ),
    path("kontakt/", views.ContactView.as_view(), name="contact"),
]
