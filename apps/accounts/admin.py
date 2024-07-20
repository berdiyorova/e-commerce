from django.contrib import admin
from django.contrib.auth.models import Group

from accounts.models import User, UserAddress


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_staff', 'is_active', 'role')


admin.site.register(User, UserAdmin)
admin.site.register(UserAddress)
