from django.contrib import admin
from django.contrib.auth.models import Group

from accounts.models import User, UserAddress

admin.site.unregister(Group)

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_staff', 'is_active')


admin.site.register(User, UserAdmin)
admin.site.register(UserAddress)
