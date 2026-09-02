from django.urls import path
from contracts.views import (ContractCreateView,
                             ContractListView,
                             ContractDetailView,
                             ContractUpdateView,
                             CloseContractView,)
app_name = "contracts"

urlpatterns = [
    path("", ContractListView.as_view(), name="contracts_list"),
    path("<int:pk>/", ContractDetailView.as_view(), name="contract_page"),
    path("<int:pk>/update/", ContractUpdateView.as_view(), name="update_contract"),
    path("<int:pk>/update/close_contract/", CloseContractView.as_view(), name="close_contract"),
    path("create_contract/", ContractCreateView.as_view(), name="create_contract"),

]