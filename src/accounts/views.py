from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from .forms import LoginForm, ProfileForm


class LoginView(SuccessMessageMixin, auth_views.LoginView):
    """A view to handle the login action."""

    template_name = "accounts/login.html"
    form_class = LoginForm
    success_message = _("Zalogowano do strony.")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)  # log out the user which is already logged in
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super().form_valid(form)


class LogoutView(auth_views.LogoutView):
    """A view to handle the logout action."""

    success_message = _("Wylogowano ze strony.")

    def dispatch(self, request, *args, **kwargs):
        """Override default dispatching method, just to pass the success message."""
        if request.user.is_authenticated:
            messages.success(request, message=self.success_message)
        return super().dispatch(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, generic.View):
    """A view to display and serve the user's profile data form."""

    template_name = "accounts/profile.html"
    success_message = _("Zapisano zmiany.")

    def get_user(self):
        return self.request.user

    def get(self, request):
        return render(
            request,
            self.template_name,
            context={
                "form": ProfileForm(instance=self.get_user()),
            },
        )

    def post(self, request):
        form = ProfileForm(
            data=request.POST,
            files=request.FILES,
            instance=self.get_user(),
        )

        if form.is_valid():
            form.save()
            messages.success(request, message=self.success_message)

            return redirect(to="accounts:profile")

        return render(request, self.template_name, context={"form": form})


class PasswordResetView(SuccessMessageMixin, auth_views.PasswordResetView):
    """A view to handle password reset action."""

    template_name = "accounts/password_reset_form.html"
    email_template_name = "accounts/password_reset_email.html"
    subject_template_name = "accounts/password_reset_email_subject.txt"
    success_url = reverse_lazy("accounts:password-reset")
    success_message = _("Wysłano instrukcję resetowania hasła.")


class PasswordResetConfirmView(
    SuccessMessageMixin,
    auth_views.PasswordResetConfirmView,
):
    """A view to handle password reset confirm action."""

    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:login")
    success_message = _("Hasło zostało zresetowane.")
    invalidlink_message = _("Nieprawidłowy link.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context["validlink"]:
            messages.warning(self.request, message=self.invalidlink_message)
        return context


class PasswordChangeView(SuccessMessageMixin, auth_views.PasswordChangeView):
    """A view to handle password change action."""

    template_name = "accounts/password_change_form.html"
    success_url = reverse_lazy("home")
    success_message = _("Ustawiono nowe hasło.")
