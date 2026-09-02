
from django.forms import ModelForm, ValidationError, SelectMultiple, CheckboxSelectMultiple

from ad_companies.models import Channel, AdCompany


class ChannelCreateForm(ModelForm):

    class Meta:
        model=Channel
        fields = ["name"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["title"]="input unique name"

    def clean_name(self):
        name = self.cleaned_data.get("name", None)
        if name is None:
            return name
        val_name=" ".join(name.split()).strip()
        if Channel.objects.filter(name__iexact=val_name).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This name is not unique for channels")
        return val_name


class AdCompanyValidateForm(ModelForm):

    class Meta:
        model=AdCompany
        fields = ["name", "budget", "connection", "channel"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["title"]="input unique name"
        self.fields["budget"].widget.attrs["title"]="input budget for the ad company"
        self.fields["connection"].widget.attrs["title"] = "choose service"
        self.fields["channel"].widget = CheckboxSelectMultiple()
        self.fields["channel"].queryset=Channel.objects.all()

    def clean_name(self):
        name= self.cleaned_data.get("name", None)
        if name is None:
            return name
        val_name = " ".join(name.split()).strip()
        if AdCompany.objects.filter(name__iexact=val_name).exclude(pk=self.instance.pk).exists():
            raise ValidationError("this name is not unique")
        return val_name