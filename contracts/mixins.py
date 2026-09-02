from contracts.models import Contract


class SortAndFilterContracts:

    def __init__(self):
        self.default_sort_by="name"
        self.default_how="asc"
        self.default_status=["1","0"]
        self.allowed_params = ["name","cost","service", "creator"]
        self.allow_how = ["asc", "desc"]
        self.model=Contract

    def get_queryset(self,*args, **kwargs):
        queryset=super().get_queryset(*args, **kwargs)
        queryset=queryset.select_related("connection", "created_by")
        self.contracts=self.model.objects.select_related("connection", "created_by").all()
        self.status = self.request.GET.get("status")
        if self.status in self.default_status:
            queryset=queryset.filter(is_finished=int(self.status))
            self.status_context = "completed" if int(self.status) else "in process"
        else:
            self.status_context = 'all'
        self.service=self.request.GET.get("connection")
        if self.service is not None and self.service.isdigit() and self.contracts.filter(pk=int(self.service)).exists():
            queryset=queryset.filter(connection=int(self.service))
        else:
            self.service='all'
        self.creator=self.request.GET.get("creator")
        if self.creator is not None and self.creator.isdigit() and self.contracts.filter(pk=int(self.creator)).exists():
            queryset=queryset.filter(created_by=int(self.creator))
        else:
            self.creator="all"
        self.sort_by=self.request.GET.get("sort_by")
        self.how=self.request.GET.get("how")
        if self.sort_by in self.allowed_params and self.how in self.allow_how:
            queryset =queryset.order_by(self.sort_by) if self.how=="asc" else queryset.order_by(f"-{self.sort_by}")
        else:
            queryset=queryset.order_by(self.default_sort_by)
            self.how=self.default_how
            self.sort_by=self.default_sort_by
        self.how_context = "up to down" if self.how=="asc" else "down to up"
        return queryset
