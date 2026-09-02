
from django.urls import path
from clients.views import (CreatePotentialClientView,
                           AllClientsListView,
                           ClientPageView,
                           ClientUpdateView,
                           CreateActiveClientView)
app_name = "clients"

urlpatterns = [
    path("",AllClientsListView.as_view(), name="clients_list"),
    path("<int:pk>/", ClientPageView.as_view(), name="client_page"),
    path("<int:pk>/update/", ClientUpdateView.as_view(), name="client_update"),
    path("<int:pk>/create_active_client/", CreateActiveClientView.as_view(), name="create_active_client_from_potential"),
    path("create_client/",CreatePotentialClientView.as_view(),name="create_pot_client"),
    path("create_active_client/", CreateActiveClientView.as_view(), name="create_active_client"),
]