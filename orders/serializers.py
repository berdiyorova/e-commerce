from rest_framework import serializers

from orders.models import *
from products.serializers import ProductSerializer


class AddToCartSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Products.objects.all(), required=True)
    quantity = serializers.IntegerField(required=True)
    attributes = serializers.ListField(child=serializers.IntegerField(min_value=1))


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ("quantity", )


class CartItemListSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        exclude = ('user',)


class OrderCreateSerializer(serializers.Serializer):
    cart_items = serializers.ListField(child=serializers.IntegerField(min_value=1))
    user_address = serializers.IntegerField(required=True)
