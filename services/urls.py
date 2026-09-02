from django.urls import path
from services.views import (ServicesListView,
                            ServiceCreateView,
                            ServiceProfileView,
                            ServiceUpdateProfileView,
                            ServiceDeleteView,
                            ChangeStatusServiceView,)


app_name = "services" #pylint: disable=C0103

urlpatterns = [
    path("",ServicesListView.as_view(), name="services_list"),
    path("create_service/", ServiceCreateView.as_view(), name = "create_service"),
    path("<int:pk>/", ServiceProfileView.as_view(), name="service_page"),
    path("<int:pk>/update/", ServiceUpdateProfileView.as_view(), name="service_update"),
    path("<int:pk>/change_status/",ChangeStatusServiceView.as_view(), name="service_change_status"),
    path("<int:pk>/delete/", ServiceDeleteView.as_view(), name="service_delete"),
]
