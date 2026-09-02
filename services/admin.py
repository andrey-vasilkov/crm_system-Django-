from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from services.models import Service
# Register your models here.

@admin.register(Service)
class AdminService(admin.ModelAdmin):
    """Show services on admin panel"""
    list_display = ["name", "description", "price", "creator", "modifier"]
    search_fields = ["name", "created_by__username", "modified_by__username"]

    def creator(self, obj):
        """Show service's creator"""
        if obj.created_by is None:
            return "-"
        url= reverse("admin:users_user_change", kwargs={"object_id": obj.created_by.pk})
        link = f'<a href="{url}">{obj.created_by.username}</a>'
        return mark_safe(link)

    def modifier(self, obj):
        """Show service's modifier"""
        if obj.modified_by is None:
            return "-"
        url= reverse("admin:users_user_change", kwargs={"object_id": obj.modified_by.pk})
        link = f'<a href="{url}">{obj.modified_by.username}</a>'
        return mark_safe(link)
