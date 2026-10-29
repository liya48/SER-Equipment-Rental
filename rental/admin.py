from django.contrib import admin
from .models import Supplier, Equipment, RentalRequest

admin.site.register(Supplier)
admin.site.register(Equipment)
admin.site.register(RentalRequest)

