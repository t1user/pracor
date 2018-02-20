from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^create_profile/$', views.CreateProfileView.as_view(), name='create_profile'),

    url(r'^profile/$', views.UpdateProfileView.as_view(), name='profile'),

    url(r'^register/$', views.Register.as_view(), name='register'),
    
    url(r'^register_success/$', views.RegisterSuccess.as_view(), name='register_success'),

    url(r'^complete/linkedin-oauth2/', views.LoginErrorView.as_view(), name='login_error'),

    url(r'^login/$', views.LoginCustomView.as_view(), name='login'),

    url(r'logged_out/$', views.LoggedOutView.as_view(), name='logged_out'),

    url('^password_reset/$', views.PasswordResetCustomView.as_view(), name='password_reset'),

    url('^password_reset/done/$', views.PasswordResetDoneCustomView.as_view(), name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.PasswordResetConfirmCustomView.as_view(), name='password_reset_confirm'),

    url(r'^reset/done/$', views.PasswordResetCompleteCustomView.as_view(), name='password_reset_complete'),

    url(r'password_change/$', views.PasswordChangeCustomView.as_view(), name='password_change'),

    url(r'password_change/done/$', views.PasswordChangeDoneCustomView.as_view(), name='password_change_done'),

    url(r'^account_activation_sent/$', views.AccountActivationSentView.as_view(), name='account_activation_sent'),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.AccountActivateView.as_view(), name='activate'),

    url(r'^email_not_confimed/$', views.EmailConfirmReminderView.as_view(), name='email_confirm_reminder'),

    url(r'^activation_email_send_again/$', views.ActivationEmailSendAgain.as_view(), name='activation_email_send_again'),

    url(r'auth_error/$', views.SocialAuthErrorView.as_view(), name='auth_error'),

    url(r'set_password/$', views.SocialAuthSetPassword.as_view(), name='set_password'),
]
