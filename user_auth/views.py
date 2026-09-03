from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from config.settings import LOGOUT_REDIRECT_URL

# Create your views here.


class AuthMainView(TemplateView):
    """Show main page depending on authenticated"""
    def get_template_names(self):
        """Select template depending on authenticated"""
        if self.request.user.is_authenticated:
            return "auth/auth_main_auth.html"
        return "auth/auth_main_notauth.html"

    def get_context_data(self, **kwargs):
        """return context"""
        user = self.request.user.username
        pk=self.request.user.pk
        context = {
            "user":user,
            "pk":pk,
        }
        return context

class AuthLoginView(LoginView):
    """Login user"""
    template_name = "auth/auth_login.html"


class UsersChangePassView(PasswordChangeView):
    """Change user's pssword'"""
    template_name = "auth/auth_change_pass.html"
    success_url = reverse_lazy("auth:login")

def authlogout(request:HttpRequest) -> redirect:
    """Logout user"""
    logout(request)
    return redirect(LOGOUT_REDIRECT_URL)
