from django import forms
from django.urls import reverse_lazy

# Create your views here.
from django.views.generic import CreateView, ListView, UpdateView, DetailView


from clients.forms import ValidateCreatePotentialClient, ValidateUpdatePotentialClient
from clients.mixins import ClientsSortAndFilter
from clients.models import PotentialClient, ActiveClient
from common_files.mixins import CheckAccessMixin
from contracts.models import Contract
from logging_setup import logger


class CreatePotentialClientView(CheckAccessMixin,CreateView):
    """Create potential client"""
    model = PotentialClient
    required_perm = "clients.add_potentialclient"
    form_class = ValidateCreatePotentialClient
    template_name = "clients/create_client.html"
    success_url = reverse_lazy("clients:clients_list")

    def form_valid(self, form):
        form.instance.created_by=self.request.user
        response=super().form_valid(form)
        logger.info(f"{self.request.user.username} create a new potential client: {self.object}")
        return response

class AllClientsListView(CheckAccessMixin,ClientsSortAndFilter,ListView):
    "Show clients list depends on user permissions"
    required_perm = None
    model = PotentialClient

    def get_extra_param(self):
        """return extra param needed for template choice and user perms"""
        user_perms=self.request.user.get_all_permissions()
        if self.request.user.is_superuser or "clients.view_all_clients_list" in user_perms:
            extra_param="all_clients"
        elif "clients.view_clients_list" in user_perms:
            extra_param="potential_clients"
        else:
            extra_param="error"
        return extra_param, user_perms



    def get_template_names(self):
        extra_param, _=self.get_extra_param()
        if extra_param == "all_clients":
            return "clients/all_clients_list.html"
        if extra_param == "potential_clients":
            return "clients/potential_clients_list.html"
        return "errors/AccessDenied.html"


    def get_queryset(self, *args, **kwargs):
        queryset=super().get_queryset(*args, **kwargs)
        queryset=queryset.select_related("active_client","ad_company__connection").all()
        return queryset

    def get_context_data(self, *args, **kwargs): #pylint: disable=R0914
        extra_param, user_perms =self.get_extra_param()
        if extra_param == "error":
            error = "You don't have enough permissions"
            perms = user_perms
            required_perms="clients.view_all_clients_list or clients.view_clients_list"
            logger.warning(f"{self.request.user.username} try to visit {self.request.path}."
                           f"But doesn't have enough permissions")
            context = {
                "error": error,
                "perms": perms,
                "req": required_perms,
            }
            return context

        # pylint: disable=W0201
        context=super().get_context_data(*args,**kwargs)
        all_potential_clients_list=context["object_list"]
        context["status"]={"Potential clients":[],
                           "Active clients":[]}
        for client in all_potential_clients_list:
            if hasattr(client, "active_client"):
                context["status"]["Active clients"].append(client)
            else:
                context["status"]["Potential clients"].append(client)

        if extra_param == "potential_clients":
            self.status = "potential"
        if self.status == "potential":
            context["status"]["Active clients"]=[]
        elif self.status == "active":
            context["status"]["Potential clients"] = []
        context["companies"]=self.all_companies
        context["services"]=self.all_services
        if self.company=="all":
            chosen_company=self.company
        else:
            company = self.all_companies.filter(pk=int(self.company)).first()
            chosen_company=company.name if company else "all"
        if self.service == "all":
            chosen_service=self.service
        else:
            service = self.all_services.filter(pk=int(self.service)).first()
            chosen_service = service.name if service else "all"
        chosen_status="clients" if extra_param=="potential_clients" else self.status
        chosen_params=(f"Status: {chosen_status}, "
                       f"Ad company: {chosen_company},"
                       f"Service: {chosen_service}, "
                       f"Sort by: {self.sort_by_context}, "
                       f"How: {self.how_context} ")
        context["chosen_params"]=chosen_params
        return context



class ClientPageView(CheckAccessMixin,DetailView):
    """Show client profile"""
    template_name = "clients/client_page.html"
    required_perm = "clients.view_potentialclient"
    model = PotentialClient

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["active"]=ActiveClient.objects.filter( #pylint: disable=E1101
            client=self.object.pk).first()
        context["can_change_potential"] = \
            self.request.user.has_perm("clients.change_potentialclient")
        context["can_change_active"] = self.request.user.has_perm("clients.change_activeclient")
        context["is_super"]=self.request.user.is_superuser
        return context

class ClientUpdateView(CheckAccessMixin,UpdateView):
    """Update client profile"""
    required_perm = "clients.change_potentialclient"
    model = PotentialClient
    form_class = ValidateUpdatePotentialClient
    template_name = "clients/update_client.html"

    def get_success_url(self):
        return reverse_lazy("clients:client_page", kwargs={"pk":self.object.pk})


class CreateActiveClientView(CheckAccessMixin, CreateView):
    """Change potential client to active"""
    required_perm = "clients.add_activeclient"
    model = ActiveClient
    fields = ["client", "contract"]
    template_name = "clients/create_active_client.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args,**kwargs)
        # pylint: disable=W0201
        self.client = self.get_potential_client()


    def get_success_url(self):
        if self.client:
            response = reverse_lazy("clients:client_page", kwargs={"pk":self.client.pk})
            return response
        response = reverse_lazy("clients:clients_list")
        return response

    def get_potential_client(self):
        """return potential client from url pk or None"""
        potential_client_pk=self.kwargs.get("pk")
        try:
            potential_client=PotentialClient.objects.filter( #pylint: disable=E1101
                pk=potential_client_pk).first()
            return potential_client
        except PotentialClient.DoesNotExist: #pylint: disable=E1101
            return None

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        if self.client:
            context["client"]=self.client
            return context
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        actives = ActiveClient.objects.all() #pylint: disable=E1101
        exclude_contracts = [active.contract.pk for active in actives]
        if self.client:
            form.fields["client"].widget = forms.HiddenInput()
            form.fields["client"].initial=self.client
            form.fields["contract"].queryset = (Contract.objects. #pylint: disable=E1101
                                                filter(
                                                    connection=self.client.ad_company.connection).
                                                exclude(pk__in=exclude_contracts).
                                                all())
        else:
            exclude_pk=[active.client.pk for active in actives ]
            form.fields["client"].queryset=PotentialClient.objects.exclude( #pylint: disable=E1101
                pk__in=exclude_pk).all()
            form.fields["contract"].queryset = (Contract.objects. #pylint: disable=E1101
                                                exclude(pk__in=exclude_contracts).
                                                all())

        return form

    def form_valid(self, form):
        response=super().form_valid(form)
        logger.info(f"""{self.request.user.username} make active client:
{self.object.client.full_name()}""")
        return response
