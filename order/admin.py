from django.contrib import admin

from order.models import Order, Item


admin.site.register(Order)
admin.site.register(Item)
