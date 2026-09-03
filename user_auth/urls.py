from django.urls import path

from user_auth.views import AuthLoginView, AuthMainView, UsersChangePassView, authlogout

app_name = "auth" #pylint: disable=C0103

urlpatterns = [
    path("",AuthMainView.as_view(), name="main"),
    path("login/", AuthLoginView.as_view(),name="login"),
    path("logout/", authlogout, name="logout"),
    path("change_pass/", UsersChangePassView.as_view(), name="change_pass"),
]
