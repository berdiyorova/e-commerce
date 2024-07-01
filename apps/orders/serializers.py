from rest_framework import serializers

# # `import *` qilish yaxshi kodmas...
from orders.models import (
    AttributeValue, CartItem, Products,
)
from products.serializers import ProductSerializer


class AddToCartSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        # bu yerda get_Serializer_context dagi qaytgan qiymatlarni qo'shdim
        self.request = kwargs.pop('request')
        self.view = kwargs.pop('view')
        self.user = kwargs.pop('user')

        super().__init__(*args, **kwargs)

    product = serializers.PrimaryKeyRelatedField(queryset=Products.objects.all(), required=True)
    quantity = serializers.IntegerField(required=True)
    # attributes = serializers.ListField(child=serializers.IntegerField(min_value=1))

    # # Validatsiya uchun ListField ni o'rniga ishlatganingiz yaxshiroq bo'lishi mumkin.
    # # Ishlaydi deb o'ylayman, lekin tekshriib ko'rish kerak.
    attributes = serializers.PrimaryKeyRelatedField(queryset=AttributeValue.objects.all())

    def validate(self, attrs):
        """
        Client yuborgan ma'lumotlarni qayta ishlaydi,
        kerakli tekshiruvlarni qilsak bo'ladi.
        """
        # # Biz faqat attribute va subtotal ni tekshirishimiz kerak 
        # # attributes -bu aniq AttributeValue ni objectlari. drf o'zi
        # validatsiya qiladi
        # # biz faqat attribute shu productga tegishli ekanligini tekshiramiz.
        attributes = attrs['attributes']
        product = attrs['product']

        # # Tekshirish kerak: attributes - objectlarni listimi yoki id larni listimi?
        # # print(attributes)
        # # if object larni listi bo'lsa:
        subtotal = 0
        for attribute in attributes:
            if attribute.product != product:
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
        methodlardan birini chaqiradi. (ModelSerializer larda shunday)
            >>> serializer.save(user=request.user) qilgandim. 
            bu yerda validated_data ga `user` key bilan request.user ni qo'shib qo'shayapti, ya'ni:
            >>>  kwargs = {"user": request.user} # bu yerda
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

    # lekin, agar update method ni ishlatmasangiz yozish shart emas.
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
