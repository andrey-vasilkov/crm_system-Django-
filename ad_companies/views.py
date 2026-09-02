
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Count, Sum
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from ad_companies.models import AdCompany,Channel
from ad_companies.forms import ChannelCreateForm, AdCompanyValidateForm
from common_files.mixins import CheckAccessMixin, SortAndFilterMixin
from logging_setup import logger


class ChannelCreateView(CheckAccessMixin,CreateView):
    """Create a new channel for ads"""
    form_class = ChannelCreateForm
    required_perm = "ad_companies.add_channel"
    template_name = "ads/channel_create.html"
    success_url = reverse_lazy("ads:channels_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f"{self.request.user.username} create channel: {self.object.name}")
        return response

class AdCompanyCreateView(CheckAccessMixin,CreateView):
    """Create a new ad company"""
    form_class = AdCompanyValidateForm
    required_perm = "ad_companies.add_adcompany"
    template_name = "ads/ad_create.html"
    success_url = reverse_lazy("ads:ads_list")

    def form_valid(self, form):
        form.instance.created_by=self.request.user
        form.instance.modified_by=form.instance.created_by
        response = super().form_valid(form)
        logger.info(f"{self.request.user.username} create ad company: {self.object.name}")
        return response

class ChannelsListView(CheckAccessMixin,ListView):
    """Show all or  filter/sort channels"""
    model = Channel
    required_perm = "ad_companies.view_channels_list"
    template_name = "ads/channels_list.html"


class AdCompaniesListView(CheckAccessMixin,SortAndFilterMixin,ListView):
    """Show all or filter/sort ad companies"""
    model = AdCompany
    required_perm = "ad_companies.view_ads_list"
    template_name = "ads/ads_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("connection", "created_by").prefetch_related("channel")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        ad_companies = context["object_list"]
        context["status"]={"active":[],
                           "archived":[]}
        for company in ad_companies:
            if company.is_active:
                context["status"]["active"].append(company)
            else:
                context["status"]["archived"].append(company)
        queryset=(AdCompany.objects.select_related("created_by").
                  prefetch_related("channel").
                  select_related("connection").all())
        creators = set([company.created_by for company in queryset])
        context["creators"] = creators
        channels=[company.channel.all() for company in queryset]
        unique_channels = set([unique for channel in channels for unique in channel])
        context["channels"]=unique_channels
        services={company.connection for company in queryset}
        context["services"]=services
        if self.service=="all":
            choosen_service=self.service
        else:
            service=queryset.filter(connection=self.service).first()
            choosen_service = service.connection.name if service else "all"
        if self.channel=="all":
            choosen_channel=self.channel
        else:
            channel=Channel.objects.filter(pk=self.channel).first()
            choosen_channel = channel.name if channel else "all"
        if self.creator == "all":
            choosen_creator = self.creator
        else:
            result=queryset.filter(created_by=self.creator).first()
            choosen_creator=result.created_by.username if result else "all"
        choosen_params=(f"Status: {self.status_context}, "
                        f"service: {choosen_service}, "
                        f"channel: {choosen_channel}, "
                        f"creator: {choosen_creator}, "
                        f"sort by: {self.sort_by}, "
                        f"how: {"up to down" if self.how=="asc" else "down to up"}")
        context["choosen_params"]=choosen_params
        return context

class AdCompanyPageView(CheckAccessMixin,DetailView):
    """Show ad company page"""
    model = AdCompany
    required_perm = "ad_companies.view_adcompany"
    template_name = "ads/ad_page.html"

class AdCompanyUpdateView(CheckAccessMixin,UpdateView):
    """Update ad company"""
    model = AdCompany
    required_perm = "ad_companies.change_adcompany"
    template_name = "ads/ad_update.html"
    form_class = AdCompanyValidateForm

    def get_success_url(self):
        response = reverse_lazy("ads:ad_page", kwargs={"pk":self.object.pk})
        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f"{self.request.user.username} update ad company: {self.object.name}")
        return response

class ChangeStatusAdCompanyView(CheckAccessMixin,DetailView):
    """Change status ad company to active/archived"""
    model = AdCompany
    required_perm = "ad_companies.change_adcompany"

    def post(self, request, pk):
        object = self.get_object()
        object.is_active = not object.is_active
        object.save()
        logger.warning(f"{self.request.user.username} change {object.name}'status to {object.is_active}")
        response = reverse_lazy("ads:ad_page", kwargs = {"pk": object.pk})
        return redirect(response)

class ChannelDeleteView(CheckAccessMixin,DeleteView):
    """Delete channel"""
    model = Channel
    required_perm = "ad_companies.delete_channel"
    def post(self, request, pk):
        channel = self.get_object()
        channel.delete()
        logger.warning(f"{request.user.username} delete {channel.name}")
        response = reverse_lazy("ads:channels_list")
        return redirect(response)

class AdDeleteView(CheckAccessMixin,DeleteView):
    """Delete ad company"""
    model = AdCompany
    required_perm = "ad_companies.delete_adcompany"
    template_name = "ads/ad_delete.html"
    success_url = reverse_lazy("ads:ads_list")

    def form_valid(self, form):
        object=self.get_object()
        response = super().form_valid(form)
        logger.warning(f"{self.request.user.username} delete ad company: {object.name}")
        return response


class AdCompanyStatisticView(LoginRequiredMixin,ListView):
    """Show statistic"""
    template_name = "ads/ads_statistic.html"
    model = AdCompany

    def get_statistic_data(self):
        """count statistic"""
        ads = AdCompany.objects.annotate(
            potential=Count("potentialclient", distinct=True),
            active=Count("potentialclient__active_client", distinct=True),
            contracts=Sum("potentialclient__active_client__contract__agreed_cost", distinct=True),
        )
        for ad in ads:
            ad.contracts_sum = ad.contracts if ad.contracts else 0
            ad.ratio = round(ad.contracts_sum/ad.budget,3) if ad.budget else 0
        return ads

    def get_context_data(self, *args, **kwargs):
        """create context"""
        context = super().get_context_data(*args, **kwargs)
        context["ads"]=self.get_statistic_data()
        return context



