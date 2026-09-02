from django.contrib.admindocs.views import extract_views_from_urlpatterns
from django.core.exceptions import ValidationError
from django.db import connection
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from contracts.models import Contract, ExtraFilesToContract
from contracts.forms import ContractValidateForm, ContractValidateUpdateForm, ContractUploadExtraFilesForm
from common_files.mixins import CheckAccessMixin
from contracts.mixins import SortAndFilterContracts
from logging_setup import logger

# Create your views here.


class ContractCreateView(CheckAccessMixin,CreateView):
    """Create a new contract"""
    model=Contract
    template_name = "contracts/contract_create.html"
    required_perm = "contracts.add_contract"
    form_class = ContractValidateForm
    success_url = reverse_lazy("contracts:contracts_list")

    def form_valid(self, form):
        form.instance.created_by=self.request.user
        response = super().form_valid(form)
        logger.info(f"{self.request.user.username} create contract {self.object.name}")
        return response

class ContractListView(CheckAccessMixin,SortAndFilterContracts,ListView):
    model = Contract
    required_perm = "contracts.view_contracts_list"
    template_name = "contracts/contract_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["status"]={"processing":[],
                           "completed":[]}
        for object in context["object_list"]:
            if object.is_finished:
                context["status"]["completed"].append(object)
            else:
                context["status"]["processing"].append(object)
        services = set([contract.connection for contract in self.contracts ])
        context["services"]=services
        if self.service == "all":
            chosen_service=self.service
        else:
            contract=self.contracts.filter(connection=self.service).first()
            chosen_service=contract.connection.name if contract else "all"
        creators = {contract.created_by for contract in self.contracts}
        context["creators"]=creators
        if self.creator =="all":
            chosen_creator=self.creator
        else:
            contract=self.contracts.filter(created_by=int(self.creator)).first()
            chosen_creator=contract.created_by.username if contract else "all"
        context["chosen_params"]=(f"Status: {self.status_context}, "
                                  f"service: {chosen_service}, "
                                  f"cretor: {chosen_creator},"
                                  f"sort by: {self.sort_by}, "
                                  f"how: {self.how_context}")
        return context


class ContractDetailView(CheckAccessMixin,DetailView):
    """Show contract profile"""
    model = Contract
    required_perm = "contracts.view_contract"
    template_name = "contracts/contract_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_files = ExtraFilesToContract.objects.filter(contract=self.object.pk)
        context["extra_files"]=extra_files
        return context

class ContractUpdateView(CheckAccessMixin,UpdateView):
    """Update contract"""
    model=Contract
    required_perm = "contracts.change_contract"
    template_name = "contracts/contract_update.html"
    form_class = ContractValidateUpdateForm
    extra_form_class=ContractUploadExtraFilesForm

    def get_form(self, form_class=form_class):
        if self.request.POST:
            return form_class(self.request.POST, instance=self.object)
        return form_class

    def get_extra_form(self, form_class=extra_form_class):
        if self.request.POST:
            return form_class(self.request.POST, self.request.FILES)
        return form_class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"]=self.get_form()
        context["extra_form"]=self.get_extra_form()
        return context



    def post(self, request, *args,**kwargs):
        self.object=self.get_object()
        main_form=self.get_form()
        extra_form=self.get_extra_form()
        if main_form.is_valid() and extra_form.is_valid():
            return self.form_valid(main_form,extra_form)
        return self.form_invalid(main_form,extra_form)

    def get_success_url(self):
        response = reverse_lazy("contracts:contract_page", kwargs={"pk":self.object.pk})
        return response

    def form_valid(self, main_form, extra_form):
        extra_form.instance.contract=self.object
        self.object=main_form.save()
        extra_form.save()
        logger.info(f"{self.request.user.username} update {self.object.name}")
        return redirect(self.get_success_url())

    def form_invalid(self, main_form, extra_form):
        return self.render_to_response(
            context=self.get_context_data(
                form=main_form,
                extra_form=extra_form
            ),

        )

class CloseContractView(CheckAccessMixin,UpdateView):
    """Make up contract as completed"""
    model = Contract
    required_perm = "contracts.close_contract"
    template_name = "contracts/contract_close.html"
    fields = []
    success_url = reverse_lazy("contracts:contracts_list")

    def form_valid(self, form):
        self.object.is_finished=True
        response = super().form_valid(form)
        logger.info(f"{self.request.user.username} close the contract {self.object.name}")
        return response



