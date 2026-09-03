from django.urls import path

from users.views import (
                         ChangeStatusUserView,
                         CreateUserView,
                         UpdateUserView,
                         UsersListView,
                         UsersPageView,
)

app_name = "users" #pylint: disable=C0103

urlpatterns = [
    path("", UsersListView.as_view(), name="users_list" ),
    path("<int:pk>/", UsersPageView.as_view(), name="user_page"),
    path("<int:pk>/update", UpdateUserView.as_view(), name="user_update"),
    path("<int:pk>/update/change_status/", ChangeStatusUserView.as_view(),
         name = "user_change_status"),
    path("createuser/", CreateUserView.as_view(), name="create_user"),
]
