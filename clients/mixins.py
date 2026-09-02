from ad_companies.models import AdCompany
from services.models import Service


class ClientsSortAndFilter:

    def __init__(self):
        self.default_sort_by="id"
        self.allowed_sort_by={"id": "Number",
                              "last_name": "Name"}
        self.default_how="asc"
        self.allowed_how={"asc":"Up to down",
                          "desc": "Down to up"}
        self.allowed_statuses=["potential","active"]

    def get_queryset(self,*args,**kwargs):
        queryset=super().get_queryset(*args,**kwargs)
        self.status=self.request.GET.get("status")
        self.all_companies = AdCompany.objects.select_related("connection").all()
        self.all_services=Service.objects.all()
        if self.status not in self.allowed_statuses:
            self.status ="all"
        self.company=self.request.GET.get("ad_company")
        if self.company is not None and self.company.isdigit() and self.all_companies.filter(pk=int(self.company)).exists():
            queryset=queryset.filter(ad_company=int(self.company))
        else:
            self.company ="all"
        self.service=self.request.GET.get("service")
        if self.service is not None and self.service.isdigit() and self.all_services.filter(pk=int(self.service)).exists():
            queryset = queryset.filter(ad_company__connection=int(self.service))
        else:
            self.service = "all"
        self.sort_by=self.request.GET.get("sort_by")
        self.how=self.request.GET.get("how")
        if  self.sort_by not in self.allowed_sort_by.keys() or self.how not in self.allowed_how.keys():
            self.sort_by=self.default_sort_by
            self.how=self.default_how
        queryset = queryset.order_by(self.sort_by) if self.how == "asc" else queryset.order_by(f"-{self.sort_by}")
        self.sort_by_context=self.allowed_sort_by[self.sort_by]
        self.how_context=self.allowed_how[self.how]
        return queryset


