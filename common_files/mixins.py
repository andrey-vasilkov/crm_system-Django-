from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import render


from logging_setup import logger



class CheckSuperUser(AccessMixin):
    """Check is profile belonging to superuser"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        object=self.get_object()
        if object.is_superuser:
            logger.warning(f"""{request.user.username} try to update {object.username}'s profile.
But {object.username} is superuser. Not enough permissions""")
            error = f"You can't update {object.username}'s profile"
            context = {
                "error":error,
            }
            return render(request,
                          "errors/UpdateSuperDenied.html",
                          context=context)
        return super().dispatch(request, *args, **kwargs)

class CheckAccessMixin(AccessMixin):
    """Check user's permissions to visit page"""
    required_perm = None
    login_url = "auth:login"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        user_perms=request.user.get_all_permissions()
        if self.required_perm is None or self.required_perm.lower() in user_perms:
            return super().dispatch(request, *args,**kwargs)
        error="You don't have enough permissions"
        perms = request.user.get_all_permissions()
        logger.warning(f"{request.user.username} try to visit {request.path}."
                       f"But doesn't have enough permissions")
        context = {
            "error":error,
            "perms":perms,
            "req": self.required_perm,
        }
        response=render(request,"errors/AccessDenied.html", context=context)
        return response

class SortAndFilterMixin:

    def get_queryset(self):
        queryset=super().get_queryset()
        self.default_sort_name="id"
        self.default_sort_how="asc"
        self.allowed_names=["id","name","price","username","created_by", "budget"]
        self.allowed_status=["1", "0"]
        self.allowed_how=["asc", "desc"]
        self.sort_by=self.request.GET.get("sort_by", self.default_sort_name)
        self.how=self.request.GET.get("how", self.default_sort_how)
        self.creator=self.request.GET.get("creator")
        self.service=self.request.GET.get("service")
        self.channel=self.request.GET.get("channel")
        self.status=self.request.GET.get("status", "all")
        self.role=self.request.GET.get("role")
        if self.status in self.allowed_status:
            status=int(self.status)
            queryset=queryset.filter(is_active=status)
            self.status_context="active" if status==1 else "archived"
        else:
            self.status_context="all"
        if self.creator is not None and self.creator.isdigit():
            queryset=queryset.filter(created_by_id=self.creator)
        else:
            self.creator="all"
        if self.service is not None and self.service.isdigit():
            queryset=queryset.filter(connection=self.service)
        else:
            self.service="all"
        if self.channel is not None and self.channel.isdigit():
            queryset=queryset.filter(channel=self.channel)
        else:
            self.channel="all"
        if self.role is not None and self.role.isdigit():
            queryset=queryset.filter(groups=self.role)
        else:
            self.role="all"
        if self.sort_by in self.allowed_names and self.how in self.allowed_how:
            queryset = queryset.order_by(self.sort_by) if self.how=="asc" else queryset.order_by(f"-{self.sort_by}")
            return queryset
        queryset = queryset.order_by(self.default_sort_name)

        return queryset