from django.urls import path, re_path

from . import views

urlpatterns = [
    path("create_profile/", views.CreateProfileView.as_view(), name="create_profile"),
    path("profile", views.UpdateProfileView.as_view(), name="profile"),
    path("register", views.Register.as_view(), name="register"),
    path("register_success/", views.RegisterSuccess.as_view(), name="register_success"),
    path(
        "complete/linkedin-oauth2/", views.LoginErrorView.as_view(), name="login_error"
    ),
    path("login/", views.LoginCustomView.as_view(), name="login"),
    path("logged_out/", views.LoggedOutView.as_view(), name="logged_out"),
    path(
        "password_reset/",
        views.PasswordResetCustomView.as_view(),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        views.PasswordResetDoneCustomView.as_view(),
        name="password_reset_done",
    ),
    re_path(
        r"^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        views.PasswordResetConfirmCustomView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteCustomView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "password_change/",
        views.PasswordChangeCustomView.as_view(),
        name="password_change",
    ),
    path(
        "password_change/done/",
        views.PasswordChangeDoneCustomView.as_view(),
        name="password_change_done",
    ),
    path(
        "account_activation_sent/",
        views.AccountActivationSentView.as_view(),
        name="account_activation_sent",
    ),
    re_path(
        r"^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        views.AccountActivateView.as_view(),
        name="activate",
    ),
    path(
        "email_not_confimed/",
        views.EmailConfirmReminderView.as_view(),
        name="email_confirm_reminder",
    ),
    path(
        "activation_email_send_again/",
        views.ActivationEmailSendAgain.as_view(),
        name="activation_email_send_again",
    ),
    path("auth_error/", views.SocialAuthErrorView.as_view(), name="auth_error"),
    path("set_password/", views.SocialAuthSetPassword.as_view(), name="set_password"),
]
