from django.conf.urls import url

from .views import (CreateProfileView, Register, AccountActivationSentView,
                    AccountActivateView, RegisterSuccess, LoginErrorView,
                    LoginCustomView, LoggedOutView, PasswordResetCustomView,
                    PasswordResetDoneCustomView, PasswordResetConfirmCustomView,
                    PasswordResetCompleteCustomView, PasswordChangeCustomView,
                    PasswordChangeDoneCustomView)


urlpatterns = [
    url(r'^create_profile/$',
        CreateProfileView.as_view(), name='create_profile'),

    url(r'^register/$', Register.as_view(), name='register'),
    
    url(r'^register_success/$', RegisterSuccess.as_view(), name='register_success'),

    url(r'^complete/linkedin-oauth2/', LoginErrorView.as_view(), name='login_error'),

    url(r'^login/$', LoginCustomView.as_view(), name='login'),

    url(r'logged_out/$', LoggedOutView.as_view(), name='logged_out'),

    url('^password_reset/$', PasswordResetCustomView.as_view(), name='password_reset'),

    url('^password_reset/done/$', PasswordResetDoneCustomView.as_view(), name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmCustomView.as_view(), name='password_reset_confirm'),

    url(r'^reset/done/$', PasswordResetCompleteCustomView.as_view(), name='password_reset_complete'),

    url(r'password_change/$', PasswordChangeCustomView.as_view(), name='password_change'),

    url(r'password_change/done/$', PasswordChangeDoneCustomView.as_view(), name='password_change_done'),

    url(r'^account_activation_sent/$', AccountActivationSentView.as_view(), name='account_activation_sent'),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        AccountActivateView.as_view(), name='activate'),
]
