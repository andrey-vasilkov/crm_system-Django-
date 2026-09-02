from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.conf import settings


# Create your models here.

class Service(models.Model):
    """Describe service"""
    name = models.CharField(verbose_name="Name",
                            max_length=20,
                            null=False,
                            blank=False)
    description = models.TextField(verbose_name="Description",
                                   null=False,
                                   blank=False,
                                   max_length=500)
    price = models.DecimalField(verbose_name="Price",
                                null=False,
                                blank=False,
                                max_digits=10,
                                decimal_places=2,
                                validators=[MinValueValidator(1)],
                                )
    created_by = models.ForeignKey(verbose_name="Creator",
                                   to=settings.AUTH_USER_MODEL,
                                   on_delete=models.SET_NULL,
                                   blank=True,
                                   null=True,
                                   related_name="service_creator")

    created = models.DateField(verbose_name="Created data",
                               auto_now_add=True)
    modified_by = models.ForeignKey(verbose_name="last modifier",
                                    to=settings.AUTH_USER_MODEL,
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    blank=True,
                                    related_name="service_modifier")
    modified = models.DateField(verbose_name="Last update",
                                auto_now=True)
    is_active=models.BooleanField(verbose_name="active",
                                  default=True)
    class Meta: #pylint: disable=C0115,R0903
        permissions = [
            ("services_list_view","Can view services list"),
        ]
    def get_fields(self):
        """Get name and value service's fields"""
        fields = {
            "id":self.pk,
            "Name":self.name,
            "Description":self.description,
            "Price":self.price,
            "Creator":self.created_by,
            "Created data":self.created,
            "Last modifier":self.modified_by,
            "Last modify data": self.modified,
            "Active":self.is_active,
        }
        return fields

    def __str__(self):
        return self.name.title()

    def get_absolute_url(self):
        """get url to service unit page"""
        path=reverse("services:service_page", kwargs= {"pk":self.pk})
        return path

    def save(self, *args,**kwargs):
        norm_name=self.name.strip()
        self.name=" ".join(norm_name.split())
        super().save(*args,**kwargs)
