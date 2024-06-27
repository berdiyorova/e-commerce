from django.contrib import admin

from products.models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'category_name')
    prepopulated_fields = {'slug': ('category_name',)}

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('category', 'product_name')


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('product', 'name')


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('attribute', 'value', 'price')


admin.site.register(Discount)
