from ad_companies.models import AdCompany
from services.models import Service


class ClientsSortAndFilter: #pylint: disable=R0902,R0903
    """Sort and filter clients list"""
    def __init__(self): #pylint: disable=C0116
        self.default_sort_by="id"
        self.allowed_sort_by={"id": "Number",
                              "last_name": "Name"}
        self.default_how="asc"
        self.allowed_how={"asc":"Up to down",
                          "desc": "Down to up"}
        self.allowed_statuses=["potential","active"]

    def get_queryset(self,*args,**kwargs):
        """return sorted and filtered queryset"""
        # pylint: disable=W0201
        queryset=super().get_queryset(*args,**kwargs) #pylint: disable=E1101
        self.status=self.request.GET.get("status") #pylint: disable=E1101
        self.all_companies = AdCompany.objects.select_related("connection").all() #pylint: disable=E1101
        self.all_services=Service.objects.all() #pylint: disable=E1101
        if self.status not in self.allowed_statuses:
            self.status ="all"
        self.company=self.request.GET.get("ad_company") #pylint: disable=E1101
        if (self.company is not None and self.company.isdigit()
                and self.all_companies.filter(pk=int(self.company)).exists()):
            queryset=queryset.filter(ad_company=int(self.company))
        else:
            self.company ="all"
        self.service=self.request.GET.get("service") #pylint: disable=E1101
        if (self.service is not None and self.service.isdigit()
                and self.all_services.filter(pk=int(self.service)).exists()):
            queryset = queryset.filter(ad_company__connection=int(self.service))
        else:
            self.service = "all"
        self.sort_by=self.request.GET.get("sort_by") #pylint: disable=E1101
        self.how=self.request.GET.get("how") #pylint: disable=E1101
        if self.sort_by not in self.allowed_sort_by or self.how not in self.allowed_how:
            self.sort_by=self.default_sort_by
            self.how=self.default_how
        queryset = queryset.order_by(self.sort_by) if self.how == "asc" \
            else queryset.order_by(f"-{self.sort_by}")
        self.sort_by_context=self.allowed_sort_by[self.sort_by]
        self.how_context=self.allowed_how[self.how]
        return queryset
