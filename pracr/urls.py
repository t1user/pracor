"""pracr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import RedirectView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    url(r'^', include('social_django.urls', namespace='social')),
    
    # has to be before auth, as redifines login
    url(r'^login/', LoginView.as_view(redirect_authenticated_user=True), name='login'),
    url(r'^', include('django.contrib.auth.urls')),
    
    url(r'^', include('reviews.urls')),
    
    url(r'^', include('users.urls')),

    url(r'^favicon.ico$', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico')),
                                               name='favicon'),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns

    
