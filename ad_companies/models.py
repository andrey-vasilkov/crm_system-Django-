from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from services.models import Service


# Create your models here.

class Channel(models.Model):
    """Channel of distribution"""
    name=models.CharField(verbose_name="Channel",
                          unique=True,
                          max_length=20,
                          null=False,
                          blank=False)

    class Meta: #pylint: disable=C0115,R0903
        permissions = [
            ("view_channels_list", "Can view channels list"),
        ]

    def __str__(self):
        return str(self.name)


class AdCompany(models.Model):
    """data of ad company"""


    name=models.CharField(verbose_name="Name",
                          max_length=30,
                          null=False,
                          blank=False)
    connection=models.ForeignKey(to=Service,
                                 verbose_name="Connection",
                                 null=False,
                                 blank=False,
                                 on_delete=models.CASCADE,
                                 related_name="connection")
    budget=models.DecimalField(verbose_name="Budget",
                               decimal_places=2,
                               max_digits=8,
                               null=False,
                               blank=False,
                               validators= [MinValueValidator(1)],)
    channel=models.ManyToManyField(verbose_name="Channel",
                                   to=Channel)
    created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                   verbose_name="Creator",
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL,
                                   related_name="creator")
    created_at=models.DateTimeField(verbose_name="data creating",
                                    auto_now_add=True)

    modified_by = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                   verbose_name="Modifier",
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL,
                                   related_name="modifier")
    last_modified_at = models.DateTimeField(verbose_name="data modifying",
                                      auto_now=True)
    is_active = models.BooleanField(verbose_name="active",
                                    default=True,
                                    null=False,
                                    blank=False)

    class Meta: #pylint: disable=C0115,R0903
        verbose_name="Ad Company"
        verbose_name_plural="Ad Companies"
        permissions = [
            ("view_ads_list","Can view ads list"),
        ]

    def __str__(self):
        return str(self.name)

    def get_channels(self): #pylint: disable=C0116
        channels=",".join([channel.name for channel in self.channel.all()]) #pylint: disable=E1101
        return channels

    get_channels.short_description="Channels"

    def get_fields(self): #pylint: disable=C0116
        fields = {field.verbose_name: getattr(self, field.name)
                  for field in self._meta.fields} #pylint: disable=E1101
        return fields
