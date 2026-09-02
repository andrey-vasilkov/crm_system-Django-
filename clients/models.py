from django.conf import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from ad_companies.models import AdCompany
from contracts.models import Contract


# Create your models here.

class PotentialClient(models.Model):
    """data of potential (not active) client"""
    last_name = models.CharField(verbose_name="Surname",
                            max_length=20,
                            null=False,
                            blank=False)
    first_name = models.CharField(verbose_name="Name",
                            max_length=20,
                            null=False,
                            blank=False)
    middle_name = models.CharField(verbose_name="Middle name",
                            max_length=20,
                            null=True,
                            blank=True)
    phone = PhoneNumberField(verbose_name="Phone",
                             region="RU",
                             null=False,
                             blank=False)
    email = models.EmailField(verbose_name="E-mail",
                              null=True,
                              blank=True)
    ad_company = models.ForeignKey(verbose_name="AdCompany",
                                  to=AdCompany,
                                  on_delete=models.SET_NULL,
                                  null=True)

    created_by = models.ForeignKey(verbose_name="Creator",
                                   to=settings.AUTH_USER_MODEL,
                                   related_name="potential_creator",
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True)
    created_at = models.DateTimeField(verbose_name="Creating date",
                                      null=False,
                                      blank=False,
                                      auto_now_add=True)

    class Meta: #pylint: disable=C0115,R0903
        permissions=[
            ("view_clients_list","Can view clients list"),
        ]
    def __str__(self):
        all_names = [self.last_name, self.first_name]
        if self.middle_name:
            all_names.append(self.middle_name)
        full_name=" ".join(all_names)
        return full_name

    def full_name(self): #pylint: disable=C0116
        return str(self)



class ActiveClient(models.Model):
    """data of active client with contract"""
    client=models.OneToOneField(verbose_name="Client",
                                to=PotentialClient,
                                on_delete=models.PROTECT,
                                null=False,
                                blank=False,
                                related_name="active_client")
    contract=models.OneToOneField(verbose_name="Contract",
                                  to=Contract,
                                  on_delete=models.PROTECT,
                                  null=False,
                                  blank=False)
    created_by = models.ForeignKey(verbose_name="Creator",
                                   to=settings.AUTH_USER_MODEL,
                                   related_name="active_creator",
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True)
    created_at = models.DateTimeField(verbose_name="Creating date",
                                      null=False,
                                      blank=False,
                                      auto_now_add=True)


    class Meta: #pylint: disable=C0115,R0903
        permissions = [
            ("view_all_clients_list", "can view all clients list"),
        ]
    def __str__(self):
        return str(self.client)

    def full_name(self): #pylint: disable=C0116
        return str(self)
