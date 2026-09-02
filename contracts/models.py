from pathlib import Path
import os
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from django.db import models
from services.models import Service
# Create your models here.

def create_contract_path(instance, filename):
    contract_dir=settings.MEDIA_ROOT/"contracts"/slugify(instance.connection.name)/slugify(instance.name)
    _, end = os.path.splitext(filename)
    Path(contract_dir).mkdir(parents=True, exist_ok=True)
    contract_path=contract_dir/f"contract_{instance.start_date}{end}"
    return contract_path

def uploadextrafiles(instance, filename):
    if not instance.contract.pk:
        raise ValueError("No such a contract")
    name, end = os.path.splitext(filename)
    contract_path=settings.MEDIA_ROOT/"contracts"/slugify(instance.contract.connection.name)/slugify(instance.contract.name)
    if Path(contract_path).exists():
        return contract_path/f"{slugify(name)}{end}"
    raise FileExistsError("No a directory for this contract")

class Contract(models.Model):
    name=models.CharField(verbose_name="Name",
                          max_length=20,
                          null=False,
                          blank=False)
    connection=models.ForeignKey(verbose_name="Service",
                              to=Service,
                              on_delete=models.CASCADE,
                              related_name="service")

    start_date = models.DateField(verbose_name="start",
                                  null=False,
                                  blank=False)
    finish_date = models.DateField(verbose_name="finish",
                                  null=False,
                                  blank=False)
    agreed_finish_date=models.DateField(verbose_name="Agreed date",
                                        null=True,
                                        blank=True)

    cost=models.DecimalField(verbose_name="Cost",
                             max_digits=10,
                             decimal_places=2,
                             validators=[MinValueValidator(1)],
                             )

    agreed_cost=models.DecimalField(verbose_name="Agreed cost",
                             null=True,
                             blank=True,
                             max_digits=10,
                             decimal_places=2,
                             validators=[MinValueValidator(1)],
                                    )
    is_finished=models.BooleanField(verbose_name="close",
                                    default=False)
    file=models.FileField(verbose_name="File",
                          upload_to=create_contract_path,
                          null=False,
                          blank=False)
    created_by=models.ForeignKey(verbose_name="Creator",
                                 to=settings.AUTH_USER_MODEL,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 related_name="contract_creator")
    modified_by=models.ForeignKey(verbose_name="Modifier",
                                 to=settings.AUTH_USER_MODEL,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 related_name="contract_modifier")

    class Meta:
        permissions = [
            ("close_contract", "Can close contract"),
            ("view_contracts_list","Can view contracts list"),
        ]

    def save(self, *args, **kwargs):
        if self.agreed_finish_date is None:
            self.agreed_finish_date=self.finish_date
        if self.agreed_cost is None:
            self.agreed_cost=self.cost
        if self.modified_by is None:
            self.modified_by=self.created_by
        super().save(*args,**kwargs)

    def __str__(self):
        return self.name

    def get_filename(self):
        return Path(self.file.name).name



class ExtraFilesToContract(models.Model):
    contract = models.ForeignKey(verbose_name="Contract name",
                                 to=Contract,
                                 related_name="extra_files",
                                 on_delete=models.CASCADE)
    file = models.FileField(verbose_name="extra files",
                            upload_to=uploadextrafiles,
                            null=True,
                            blank=False)

    def get_filename(self):
        return Path(self.file.name).name