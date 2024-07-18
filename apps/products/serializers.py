from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)

from products.models import Category, Products, AttributeValue, Discount


class ProductSerializer(TaggitSerializer, serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="category_name"
    )
    tags = TagListSerializerField(required=False)

    class Meta:
        model = Products
        fields = (
            "id",
            'category',
            'product_name',
            'product_image',
            'tags',
        )

    def validate(self, attrs):
        super(ProductSerializer, self).validate(attrs)
        category = attrs.get('category')
        name = attrs.get('product_name')
        if Products.objects.filter(category=category, product_name=name).exists():
            data = {
                "success": False,
                "message": "Product with this name in this category already exists."
            }
            raise ValidationError(data)
        return attrs


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'slug', 'category_name', 'category_image', 'products')


class AttributeSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Products
        fields = (
            'product',
            'name',
        )


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(read_only=True)

    class Meta:
        model = AttributeValue
        fields = (
            'attribute',
            'value',
            'image',
            'price',
        )


class DiscountSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="category_name"
    )

    class Meta:
        model = Discount
        fields = "__all__"
