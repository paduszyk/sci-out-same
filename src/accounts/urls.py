from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", view=views.LoginView.as_view(), name="login"),
    path("logout/", view=views.LogoutView.as_view(), name="logout"),
    path("profile/", view=views.ProfileView.as_view(), name="profile"),
    path(
        "password/reset/",
        view=views.PasswordResetView.as_view(),
        name="password-reset",
    ),
    path(
        "password/reset/confirm/<uidb64>/<token>/",
        view=views.PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "password/change/",
        view=views.PasswordChangeView.as_view(),
        name="password-change",
    ),
]
