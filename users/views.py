from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from common_files.mixins import CheckAccessMixin, CheckSuperUser, SortAndFilterMixin
from logging_setup import logger
from users.forms import MyCreationUserForm, MyUpdateUserForm
from users.models import User


class UsersListView(CheckAccessMixin, SortAndFilterMixin,ListView):
    """Show users list only for user with required permission"""
    template_name = "users/users_list.html"
    model = User
    required_perm="users.users_list_view"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related("groups")

    def get_context_data(self, *args, **kwargs):
        context=super().get_context_data(*args, **kwargs)
        context["users_status"]={"active users":[],
                                  "archived users":[]}
        context["groups"]=Group.objects.all().order_by("name")
        if self.role=="all":
            role_context=self.role
        else:
            role=context["groups"].filter(id=int(self.role)).first()
            role_context = role.name if role else "No such group"
        context["choosen_params"]=f"Status: { self.status_context }, role: {role_context}"
        for user in context["object_list"]:
            if user.is_active:
                context["users_status"]["active users"].append(user)
            else:
                context["users_status"]["archived users"].append(user)

        return context



class UsersPageView(CheckAccessMixin,DetailView):
    """Show user's profile"""
    template_name = "users/user_page.html"
    required_perm = "users.view_user"
    model = User

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        perms=self.object.user_permissions.all()
        self_perms=[perm.name for perm in perms]
        groups=self.object.groups.all()
        context["perms"]=self_perms
        context["groups"]=groups
        return context




class CreateUserView(CheckAccessMixin,CreateView):
    """Create a new user"""
    form_class = MyCreationUserForm
    required_perm = "users.add_user"
    model=User
    template_name ="users/create_user.html"
    success_url = reverse_lazy("users:users_list")

    def form_valid(self, form):
        form.instance.created_by=self.request.user
        response = super().form_valid(form)
        logger.info(f"Created user {self.object.username} by {self.object.created_by}")
        return response



class UpdateUserView(CheckSuperUser,CheckAccessMixin, UpdateView):
    """Update user's profile"""
    template_name = "users/update_user.html"
    required_perm = "users.change_user"
    model = User
    form_class = MyUpdateUserForm


    def get_success_url(self):
        success_url = reverse_lazy("users:user_page",kwargs={"pk":self.object.pk})
        return success_url


class ChangeStatusUserView(CheckSuperUser,CheckAccessMixin,DetailView):
    """Change status active/archived"""
    required_perm = "users.change_user"
    model = User
    def post(self, request):
        """change user's status during post request"""
        user=self.get_object()
        user.is_active=not user.is_active
        user.save()
        logger.warning(f"{request.user} change status {user} to active: {user.is_active}")
        response = reverse_lazy("users:user_page", kwargs = {"pk":user.pk})
        return redirect(response)


# Create your views here.
