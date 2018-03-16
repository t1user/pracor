from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import RedirectView
from django.contrib.sitemaps.views import sitemap
from reviews.sitemaps import (StaticViewsSitemap, CompanySitemap,)
                              #ReviewSitemap, SalarySitemap, InterviewSitemap)


sitemaps = {
    'static': StaticViewsSitemap,
    'company': CompanySitemap,
    #'review': ReviewSitemap,
    #'salary': SalarySitemap,
    #'interview': InterviewSitemap,
    }

urlpatterns = [
    url(r'^', include('social_django.urls', namespace='social')),
    
    # has to be before auth, as redifines registration views
    url(r'^', include('users.urls')),

    url(r'^', include('django.contrib.auth.urls')),
    
    url(r'^', include('reviews.urls')),

    url(r'^favicon.ico$', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico')),
                                               name='favicon'),

    url(r'pracordoc/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin', include('admin_honeypot.urls', namespace='admin_honeypot')),
    
    url(r'^pracormaster/', admin.site.urls),

    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    #url(r'^sitemap-(?P<section>.+)\.xml$', sitemap, {'sitemaps': sitemaps},
    #    name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns

    
