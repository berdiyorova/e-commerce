from rest_framework import serializers

from orders.models import CartItem
from products.models import Products, AttributeValue
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

    def save(self, **kwargs):
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


class CartItemListSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        exclude = ('user',)


class OrderCreateSerializer(serializers.Serializer):
    cart_items = serializers.ListField(child=serializers.IntegerField(min_value=1))
    user_address = serializers.IntegerField(required=True)
