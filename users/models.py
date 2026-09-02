from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ class User based on AbstractUser + field created_by"""
    created_by = models.ForeignKey("self",
                                      on_delete=models.SET_NULL,
                                      related_name="user_creator",
                                      blank=True,
                                      null=True)
    class Meta:
        permissions = [
            ("users_list_view","Can view users list"),
        ]

    def __str__(self):
        return str(self.username)

    def get_groups(self):
        """ return names of user's groups"""
        groups=",".join([group.name for group in self.groups.all()]) #pylint: disable=E1101
        return groups

    get_groups.short_description="groups"
