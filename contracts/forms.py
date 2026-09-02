from django.forms import ModelForm, ValidationError, DateInput
from contracts.models import Contract, ExtraFilesToContract


class ContractValidateForm(ModelForm):
    """Validate contract form"""
    class Meta: #pylint: disable=C0115,R0903
        model = Contract
        fields = ["name","connection", "start_date","finish_date", "cost", "file"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["title"]="input unique name"
        self.fields["connection"].widget.attrs["title"]="choose service"
        self.fields["cost"].widget.attrs["title"]="input cost of the contract"
        self.fields["start_date"].widget=DateInput(attrs={'type':"date"})
        self.fields["finish_date"].widget = DateInput(attrs={'type': "date"})
        self.fields["file"].widget.attrs["title"]="upload contract file"



    def clean(self):
        """check validate and unique name,
         validate and right dates"""
        cleaned_data=super().clean()
        name = cleaned_data.get("name", None)
        start= cleaned_data.get("start_date", None)
        finish = cleaned_data.get("finish_date", None)
        if name is None or start is None or finish is None:
            return cleaned_data
        val_name = " ".join(name.split()).strip()
        if Contract.objects.filter(name__iexact=val_name).exclude(pk=self.instance.pk).exists(): #pylint: disable=E1101
            raise ValidationError("This contract name is not unique")
        if start > finish:
            raise ValidationError("Finish date must be later than start date")
        cleaned_data["name"]=val_name

        return cleaned_data


class ContractValidateUpdateForm(ModelForm):
    """Validate form for update contract"""
    class Meta: #pylint: disable=C0115,R0903
        model=Contract
        fields = ["agreed_cost", "agreed_finish_date"]

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["agreed_finish_date"].widget = DateInput(attrs={"type":"date"})
        self.fields["agreed_finish_date"].required=False
        self.fields["agreed_cost"].required = False


    def clean_agreed_finish_date(self):
        """check new finish date"""
        finish_date=self.cleaned_data.get("agreed_finish_date")
        if finish_date is None:
            return finish_date
        if finish_date < self.instance.agreed_finish_date:
            raise ValidationError(f"New finish date must be later than "
                                  f"{self.instance.agreed_finish_date}")
        return finish_date

class ContractUploadExtraFilesForm(ModelForm):
    """Upload extra files to contract"""
    class Meta: #pylint: disable=C0115,R0903
        model = ExtraFilesToContract
        fields = ["file"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["file"].widget.attrs["title"]="Upload extra files to contract"
