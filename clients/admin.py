from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from clients.models import ActiveClient, PotentialClient

# Register your models here.

@admin.register(PotentialClient)
class PotentialClientAdmin(admin.ModelAdmin):
    """Admin view for PotentialClient"""
    list_display = ["full_name", "ad_company_profile"]
    search_fields = ["last_name","first_name", "ad_company__name"]

    def ad_company_profile(self, profile): #pylint: disable=C0116
        if profile.ad_company is None:
            return "-"
        url = reverse("admin:ad_companies_adcompany_change",
                      kwargs={"object_id":profile.ad_company.pk})
        return mark_safe(f'<a href="{url}">{profile.ad_company.name}</a>')

    ad_company_profile.short_description="Compaign"



@admin.register(ActiveClient)
class ActiveClientAdmin(admin.ModelAdmin):
    """Admin view for ActiveClient"""
    list_display = ["full_name", "contract_profile"]
    search_fields = ["client__last_name", "client__first_name"]

    def contract_profile(self, profile): #pylint: disable=C0116
        if profile.contract is None:
            return "-"
        url = reverse("admin:contracts_contract_change",
                      kwargs={"object_id":profile.contract.pk})
        return mark_safe(f'<a href="{url}">{profile.contract.name}</a>')

    contract_profile.short_description="Contract"
