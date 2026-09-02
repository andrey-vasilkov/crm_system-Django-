
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import  Group, Permission
from django import forms

from users.models import User


class MyCreationUserForm(UserCreationForm):
    """ Custom form for creating user"""
    class Meta: # pylint: disable=R0903, C0115
        model=User
        fields=["username", "email", "groups"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["title"]=self.fields[field].help_text
            self.fields[field].help_text=""
        self.fields["groups"].widget=forms.CheckboxSelectMultiple()
        self.fields["groups"].queryset=Group.objects.all()


class MyUpdateUserForm(forms.ModelForm):
    """ Custom form for updating user"""
    class Meta: # pylint: disable=R0903, C0115
        model=User
        fields=["username", "email", "groups", "user_permissions"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        exclude_perms = ["admin", "auth", "contenttypes",
                         "sessions", "messages", "staticfiles"]
        user=self.instance
        groups_perms=user.get_group_permissions()
        groups_perms_codename=[perm.split(".")[-1] for perm in groups_perms ]

        for field in self.fields:
            self.fields[field].widget.attrs["title"] = self.fields[field].help_text
            self.fields[field].help_text = ""
        self.fields["groups"].widget = forms.CheckboxSelectMultiple()
        self.fields["user_permissions"].widget = forms.CheckboxSelectMultiple()
        self.fields["groups"].queryset = Group.objects.all()
        self.fields["user_permissions"].queryset\
            =(Permission.objects
              .exclude(content_type__app_label__in=exclude_perms)
              .exclude(codename__in=groups_perms_codename))
