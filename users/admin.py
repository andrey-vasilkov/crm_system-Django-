from django.contrib import admin
from django.contrib.auth.models import Permission
from django.urls import reverse
from django.utils.safestring import mark_safe

from users.models import User

@admin.register(User)
class AdminUser(admin.ModelAdmin):
    """ Show users in admin panel"""
    list_display = ["username", "creator", "users_groups", "is_superuser"]
    search_fields = ["username", "created_by__username"]

    def creator(self, obj):
        """ Show user's creartor in admin panel"""
        if obj.created_by is None:
            return "-"
        url = reverse("admin:users_user_change", kwargs={"object_id":obj.created_by.pk})
        return mark_safe(f'<a href="{url}">{obj.created_by.username}</a>')

    def users_groups(self, obj):
        """ Show user's roles in admin panel"""
        if not obj.groups.exists():
            return "-"
        names = []
        for group in obj.groups.all():
            url=reverse("admin:auth_group_change", kwargs={"object_id":group.pk})
            name=f'<a href="{url}">{group.name}</a>'
            names.append(name)
        return mark_safe(", ".join(names))

    users_groups.short_description="Roles"


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """ Show permissions in admin panel"""
    list_display = ["name", "codename", "content_type"]
    search_fields = ["name", "content_type__app_label"]
