from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from ad_companies.models import Channel,AdCompany

# Register your models here.


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    """Admin view for Channel"""
    list_display = ["name"]
    search_fields = ["name"]

@admin.register(AdCompany)
class AdCompanyAdmin(admin.ModelAdmin):
    """Admin view for AdCompany"""
    list_display = ["name", "service", "budget", "ad_channel"]
    search_fields = ["name", "connection__name", "channel__name"]

    def service(self, company): #pylint: disable=C0116
        if company.connection is None:
            return "-"
        url = reverse("admin:services_service_change",
                      kwargs={"object_id":company.connection.pk})
        link = f'<a href="{url}">{company.connection.name}</a>'
        return mark_safe(link)

    def ad_channel(self, company): #pylint: disable=C0116
        if not company.channel.exists():
            return "-"
        links=[]
        for channel in company.channel.all():
            url = reverse("admin:ad_companies_channel_change",
                          kwargs={"object_id":channel.pk})
            link=f'<a href="{url}">{channel.name}</a>'
            links.append(link)
        return mark_safe(", ".join(links))
