
from django.forms import CheckboxSelectMultiple, ModelForm, ValidationError

from ad_companies.models import AdCompany, Channel


class ChannelCreateForm(ModelForm):
    """Form for creating channel"""

    class Meta: #pylint: disable=C0115,R0903
        model=Channel
        fields = ["name"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["title"]="input unique name"

    def clean_name(self):
        """check uniqueness of channel name"""
        name = self.cleaned_data.get("name", None)
        if name is None:
            return name
        val_name=" ".join(name.split()).strip()
        if Channel.objects.filter(name__iexact=val_name).exclude( #pylint: disable=E1101
                pk=self.instance.pk).exists():
            raise ValidationError("This name is not unique for channels")
        return val_name


class AdCompanyValidateForm(ModelForm):
    """Form for validating ad company"""

    class Meta: #pylint: disable=C0115,R0903
        model=AdCompany
        fields = ["name", "budget", "connection", "channel"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["title"]="input unique name"
        self.fields["budget"].widget.attrs["title"]="input budget for the ad company"
        self.fields["connection"].widget.attrs["title"] = "choose service"
        self.fields["channel"].widget = CheckboxSelectMultiple()
        self.fields["channel"].queryset=Channel.objects.all() #pylint: disable=E1101

    def clean_name(self):
        """check uniqueness of ad company name"""
        name= self.cleaned_data.get("name", None)
        if name is None:
            return name
        val_name = " ".join(name.split()).strip()
        if AdCompany.objects.filter(name__iexact=val_name).exclude( #pylint: disable=E1101
                pk=self.instance.pk).exists():
            raise ValidationError("this name is not unique")
        return val_name
