from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from ad_companies.models import Channel,AdCompany

# Register your models here.


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]

@admin.register(AdCompany)
class AdCompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "service", "budget", "ad_channel"]
    search_fields = ["name", "connection__name", "channel__name"]

    def service(self, object):
        if object.connection is None:
            return "-"
        url = reverse("admin:services_service_change", kwargs={"object_id":object.connection.pk})
        link = f'<a href="{url}">{object.connection.name}</a>'
        return mark_safe(link)

    def ad_channel(self, object):
        if not object.channel.exists():
            return "-"
        links=[]
        for channel in object.channel.all():
            url = reverse("admin:ad_companies_channel_change", kwargs={"object_id":channel.pk})
            link=f'<a href="{url}">{channel.name}</a>'
            links.append(link)
        return mark_safe(", ".join(links))