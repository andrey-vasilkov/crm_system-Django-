from django.forms import models

from clients.models import PotentialClient,ActiveClient

class ValidateCreatePotentialClient(models.ModelForm):

    class Meta:
        model=PotentialClient
        fields = ["last_name","first_name", "middle_name", "phone", "email", "ad_company"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["last_name"].widget.attrs["title"]="enter last name.field is required"
        self.fields["first_name"].widget.attrs["title"] = "enter first name.field is required"
        self.fields["middle_name"].widget.attrs["title"] = "enter middle name or leave empty"
        self.fields["phone"].widget.attrs["title"] = "enter phone number for RU zone.field is required"
        self.fields["email"].widget.attrs["title"] = "enter email.field is required"
        self.fields["ad_company"].widget.attrs["title"] = "choose ad company.field is required"

    def clean(self,*args,**kwargs):
        form=super().clean(*args,**kwargs)
        last_name=form.get("last_name")
        first_name=form.get("first_name")
        middle_name=form.get("middle_name")
        compaign=form.get("ad_company")
        phone=form.get("phone")
        if last_name is None or first_name is None or compaign is None or phone is None:
            return form
        val_last_name="".join(last_name).strip().title()
        val_first_name = "".join(first_name).strip().title()
        val_middle_name = "".join(middle_name).strip().title() if middle_name else None
        if PotentialClient.objects.filter(
            last_name=val_last_name,
            first_name=val_first_name,
            middle_name=val_middle_name,
            ad_company=compaign
        ).exclude(pk=self.instance.pk).exists():
            raise models.ValidationError("This potential client already exists for this ad company")
        if PotentialClient.objects.filter(phone=phone, ad_company=compaign).exclude(pk=self.instance.pk).exists():
            raise models.ValidationError("This phone number is not unique for this ad company")
        form.update(
            {"last_name":val_last_name,
             "first_name":val_first_name,
             "middle_name": val_middle_name}
        )
        return form



class ValidateUpdatePotentialClient(models.ModelForm):

    class Meta:
        model=PotentialClient
        fields = ["last_name","first_name", "middle_name", "phone", "email"]


    def clean(self,*args,**kwargs):
        form=super().clean(*args,**kwargs)
        last_name=form.get("last_name")
        first_name=form.get("first_name")
        middle_name=form.get("middle_name")
        phone=form.get("phone")
        compaign=self.instance.ad_company
        if last_name is None or first_name is None  or phone is None:
            return form
        val_last_name="".join(last_name).strip().title()
        val_first_name = "".join(first_name).strip().title()
        val_middle_name = "".join(middle_name).strip().title() if middle_name else None
        if PotentialClient.objects.filter(
            last_name=val_last_name,
            first_name=val_first_name,
            middle_name=val_middle_name,
            ad_company=compaign
        ).exclude(pk=self.instance.pk).exists():
            raise models.ValidationError("This potential client already exists for this ad company")
        if PotentialClient.objects.filter(phone=phone, ad_company=compaign).exclude(pk=self.instance.pk).exists():
            raise models.ValidationError("This phone number is not unique for this ad company")
        form.update(
            {"last_name":val_last_name,
             "first_name":val_first_name,
             "middle_name": val_middle_name}
        )
        return form



