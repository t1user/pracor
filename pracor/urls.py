from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views.generic import RedirectView

from reviews.sitemaps import CompanySitemap, StaticViewsSitemap

# ReviewSitemap, SalarySitemap, InterviewSitemap)


sitemaps = {
    "static": StaticViewsSitemap,
    "company": CompanySitemap,
    # 'review': ReviewSitemap,
    # 'salary': SalarySitemap,
    # 'interview': InterviewSitemap,
}

urlpatterns = [
    path("", include("social_django.urls", namespace="social")),
    # has to be before auth, as redifines registration views
    path("", include("users.urls")),
    path("", include("django.contrib.auth.urls")),
    path("", include("reviews.urls")),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("img/favicon.ico")),
        name="favicon",
    ),
    path("pracordoc/doc/", include("django.contrib.admindocs.urls")),
    # path("admin", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path(r"pracormaster/", admin.site.urls),
    path(
        "sitemap\.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    # url(r'^sitemap-(?P<section>.+)\.xml$', sitemap, {'sitemaps': sitemaps},
    #    name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
