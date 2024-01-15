
# Register your models here.
from django.contrib import admin
from .models import WorkOrder, ScopeOfWork, Deduction, Payment
# Register your models here.
admin.site.register(WorkOrder)
admin.site.register(ScopeOfWork)
admin.site.register(Deduction)
admin.site.register(Payment)