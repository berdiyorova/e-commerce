from django.contrib import admin

from orders.models import CartItem, Orders

admin.site.register(CartItem)
admin.site.register(Orders)
