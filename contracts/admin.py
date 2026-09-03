from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from contracts.models import Contract, ExtraFilesToContract

# Register your models here.

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    """Show contract on admin panel"""
    list_display = ["name","service","agreed_cost","agreed_finish_date", "is_finished"]
    search_fields = ["name" , "connection__name" ]

    def service(self, obj):
        """Show linked service """
        if obj.connection is None:
            return "-"
        url = reverse("admin:services_service_change", kwargs={"object_id":obj.connection.pk})
        link=f'<a href="{url}">{obj.connection.name}</a>'
        return mark_safe(link)

@admin.register(ExtraFilesToContract)
class ExtraFilesContractadmin(admin.ModelAdmin):
    """Show extra files to contract"""
    list_display = ["contract", "file"]
