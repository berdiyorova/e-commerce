from rest_framework import serializers

from orders.models import (
    AttributeValue, CartItem, Products, Orders
)
from products.serializers import ProductSerializer


class AddToCartSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.view = kwargs.pop('view')
        self.user = kwargs.pop('user')

        super().__init__(*args, **kwargs)

    product = serializers.PrimaryKeyRelatedField(queryset=Products.objects.all(), required=True)
    quantity = serializers.IntegerField(required=True)
    attributes = serializers.PrimaryKeyRelatedField(queryset=AttributeValue.objects.all(), many=True)

    def validate(self, attrs):
        """
        Client yuborgan ma'lumotlarni qayta ishlaydi,
        kerakli tekshiruvlarni qilsak bo'ladi.
        """
        attributes = attrs['attributes']
        product = attrs['product']

        subtotal = 0
        for attribute in attributes:
            if attribute.attribute.product != product:
                raise serializers.ValidationError({
                    "attributes": "Noto'g'ri attribute tanlangan: %s" % attribute.pk
                })
            else:
                subtotal += attribute.price

        attrs['subtotal'] = subtotal
        return attrs

    def save(self, **kwargs) -> Products:
        """
        Serializer ga class view da murojaat qilganda kerakli (create yoki update)
        methodlardan birini chaqiradi.
        """
        data: dict = self.validated_data
        data.update(kwargs)
        if self.instance:
            return self.update(self.instance, data)
        else:
            return self.create(data)

    def create(self, validated_data):
        attributes = validated_data.pop('attributes', [])
        self.instance = CartItem.objects.create(**validated_data)
        if attributes:
            self.instance.attributes.set(attributes)
        return self.instance

    def update(self, instance, data):
        for field, value in data.items():
            setattr(instance, field, value)
        instance.save()
        return instance


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ("quantity", )

    def get_object(self):
        cart_item = self.queryset.get(user=self.request.user, product_id=self.kwargs.get(self.lookup_field))
        return cart_item


class CartItemListSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        exclude = ('user',)


class OrderCreateSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(
        queryset=CartItem.objects.all(),
        many=True,
        pk_field=serializers.IntegerField()
    )

    class Meta:
        model = Orders
        fields = ("items", )

    def create(self, validated_data):
        items = validated_data.pop('items', [])
        self.instance = Orders.objects.create(**validated_data)
        if items:
            self.instance.items.set(items)
        return self.instance

    def total_price(self, validated_data):
        cart_items = CartItem.objects.filter(id__in=validated_data.get("items"))
        total_price = sum([item.subtotal for item in cart_items])
        return total_price
