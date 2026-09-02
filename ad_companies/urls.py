from django.urls import path
from ad_companies.views import (ChannelCreateView,
                                ChannelsListView,
                                ChannelDeleteView,
                                AdCompanyCreateView,
                                AdCompaniesListView,
                                AdCompanyPageView,
                                AdCompanyUpdateView,
                                ChangeStatusAdCompanyView,
                                AdDeleteView,
                                AdCompanyStatisticView)
app_name = "ads" #pylint: disable=C0103

urlpatterns = [
    path("",AdCompaniesListView.as_view(), name="ads_list"),
    path("statistic/", AdCompanyStatisticView.as_view(), name="ads_statistic"),
    path("<int:pk>/",AdCompanyPageView.as_view(), name="ad_page"),
    path("<int:pk>/delete_ad/", AdDeleteView.as_view(), name="ad_delete"),
    path("<int:pk>/update", AdCompanyUpdateView.as_view(), name="ad_update"),
    path("<int:pk>/update/change_status/",
         ChangeStatusAdCompanyView.as_view(), name="ad_change_status"),
    path("create_ad/", AdCompanyCreateView.as_view(), name = "create_ad"),
    path("channels/", ChannelsListView.as_view(), name="channels_list"),
    path("channels/create_channel/", ChannelCreateView.as_view(), name="create_channel"),
    path("channels/<int:pk>/delete_channel/", ChannelDeleteView.as_view(), name="delete_channel"),
]
