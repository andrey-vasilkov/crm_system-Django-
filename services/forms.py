from django.forms import ModelForm, ValidationError

from services.models import Service


class ServiceValidateForm(ModelForm):
    """Form for validate service's data"""
    class Meta: #pylint:disable=C0115,R0903
        model=Service
        fields = ["name", "description", "price"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].widget.attrs["title"]="input unique name"
        self.fields["description"].widget.attrs["title"] = "input description of the service"
        self.fields["price"].widget.attrs["title"] = "input cost of the service"


    def clean_name(self):
        """Check validate and unique name"""
        name=self.cleaned_data.get("name", None)
        if name is None:
            return name
        val_name=" ".join(name.split()).strip()
        if Service.objects.filter(name__iexact=val_name).exclude(pk=self.instance.pk).exists(): #pylint: disable=E1101
            raise ValidationError("The name isn't unique for services")
        return val_name
