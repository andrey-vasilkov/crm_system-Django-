from django.http import HttpRequest


def links_and_buttons(request:HttpRequest) -> dict:
    """provide nav links depending on user's permissions"""
    links = {
        "users.users_list_view": {"name":"users:users_list",
                                  "label": "Users list"},
        "users.add_user": {"name": "users:create_user",
                           "label":"Create user"},
        "services.services_list_view": {"name": "services:services_list",
                                  "label": "Services list"},
        "services.add_service": {"name": "services:create_service",
                                  "label": "Create service"},
        "ad_companies.view_channels_list": {"name": "ads:channels_list",
                                        "label": "Channels list"},
        "ad_companies.add_channel": {"name": "ads:create_channel",
                                  "label": "Create channel"},
        "ad_companies.view_ads_list": {"name": "ads:ads_list",
                                            "label": "Ad companies list"},
        "ad_companies.add_adcompany": {"name": "ads:create_ad",
                                     "label": "Create ad company"},
        "contracts.view_contracts_list": {"name": "contracts:contracts_list",
                                       "label": "Contracts list"},
        "contracts.add_contract": {"name": "contracts:create_contract",
                                       "label": "Create contract"},
        "clients.view_clients_list": {"name": "clients:clients_list",
                                          "label": "Potential clients list"},
        "clients.add_potentialclient": {"name": "clients:create_pot_client",
                                   "label": "Create potential client"},
        "clients.view_all_clients_list": {"name": "clients:clients_list",
                                      "label": "All clients list"},
        "clients.add_activeclient": {"name": "clients:create_active_client",
                                        "label": "Create active client"},


    }
    if not request.user.is_authenticated:
        return {"buttons": {}}
    if request.user.is_superuser:
        buttons = {link["label"]:link["name"] for link in links.values()}
        return {"buttons":buttons}
    perms = request.user.get_all_permissions()
    buttons = {links[perm]["label"]:links[perm]["name"] for perm in perms if perm in links}

    return {"buttons": buttons}
