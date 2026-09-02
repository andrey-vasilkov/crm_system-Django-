from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from services.models import Service
from services.forms import ServiceValidateForm
from logging_setup import logger
from common_files.mixins import CheckAccessMixin,SortAndFilterMixin


# Create your views here.


class ServicesListView(CheckAccessMixin,SortAndFilterMixin,ListView):
    """Show services list ith filters and sorts"""
    template_name = "services/services_list.html"
    model = Service
    required_perm = "services.services_list_view"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("created_by")

    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        services=context["object_list"]
        context["status"]={"active services":[],
                           "archived services":[]}
        for service in services:
            if service.is_active:
                context["status"]["active services"].append(service)
            else:
                context["status"]["archived services"].append(service)
        queryset = Service.objects.select_related("created_by").all() #pylint: disable=E1101
        creators = {obj.created_by for obj in queryset}
        context["creators"]=creators
        for creator in creators:
            if  self.creator == "all":
                last_filter_creator = self.creator
                break
            if creator.id==int(self.creator):
                last_filter_creator=creator.username
                break
        else:
            last_filter_creator="all"
        context["choosen_params"] = (f"Status:{self.status_context}, "
                                     f"creator:{last_filter_creator},"
                                     f"sort by:{self.sort_by}, "
                                     f"how:{"up to down" if self.how == "asc" else "down to up"}")
        return context


class ServiceCreateView(CheckAccessMixin,CreateView):
    """Create a new service"""

    required_perm = "services.add_service"
    template_name = "services/service_create.html"
    form_class = ServiceValidateForm
    success_url = reverse_lazy("services:services_list")


    def form_valid(self, form):
        form.instance.created_by=self.request.user
        form.instance.modified_by=self.request.user
        response = super().form_valid(form)
        logger.info(f"Service {self.object.name} was created by {self.object.created_by}")
        return response

class ServiceProfileView(CheckAccessMixin,DetailView):
    """Show service page"""
    model = Service
    template_name = "services/service_page.html"
    required_perm = "services.view_service"


class ServiceUpdateProfileView(CheckAccessMixin,UpdateView):
    """Update service"""
    model = Service
    template_name = "services/service_update.html"
    form_class = ServiceValidateForm
    required_perm = "services.change_service"

    def get_success_url(self):
        response = reverse_lazy("services:service_page", kwargs={"pk":self.object.pk})
        return response

    def form_valid(self, form):
        response=super().form_valid(form)
        logger.info(f"{self.request.user} updated {self.object.name}")
        return response

class ChangeStatusServiceView(CheckAccessMixin,DetailView):
    """Change service status to active/archived"""
    model=Service
    required_perm = "services.change_service"
    def post(self, request):
        """change status service during post request"""
        service=self.get_object()
        service.is_active=not service.is_active
        service.save()
        logger.warning(f"{request.user} change {service.name} status to {service.is_active}")
        response = reverse_lazy("services:service_page", kwargs={"pk":service.pk})
        return redirect(response)



class ServiceDeleteView(CheckAccessMixin,DeleteView):
    """Delete service"""
    template_name = "services/service_delete.html"
    model = Service
    success_url = reverse_lazy("services:services_list")
    required_perm = "services.delete_service"

    def form_valid(self, form):
        response=super().form_valid(form)
        logger.warning(f"{self.request.user} delete service {self.object.name}")
        return response
