from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Create default roles and assign permissions"
    def handle(self, *args, **options):
        roles = {"administrator": ["users_list_view","add_user",
                                   "change_user", "view_user"],
                 "operator": ["view_potentialclient","add_potentialclient",
                              "change_potentialclient", "view_clients_list"],
                 "manager": ["add_activeclient", "change_activeclient",
                             "view_activeclient", "view_all_clients_list",
                             "view_potentialclient", "close_contract",
                             "add_contract", "change_contract",
                             "view_contract", "view_contracts_list",
                             "add_extrafilestocontract","view_extrafilestocontract"],
                 "marketolog": ["add_adcompany","change_adcompany",
                                "view_adcompany","delete_adcompany",
                                "view_ads_list","services_list_view",
                                "add_service","change_service",
                                "view_service","delete_service",
                                "add_channel","change_channel",
                                "view_channel","delete_channel"]}
        permissions=Permission.objects.all()
        for role, perms in roles.items():
            group, created = Group.objects.get_or_create(name=role)
            if created:
                self.stdout.write(self.style.SUCCESS(f"{group.name} is created"))
            else:
                self.stdout.write(self.style.WARNING(f"{group.name} is already created"))
            role_perms=permissions.filter(codename__in=perms)
            group.permissions.add(*role_perms)
            self.stdout.write(f"group perms: {len(group.permissions.all())}")

        self.stdout.write("command is finished")
