from django_filters.rest_framework import FilterSet, filters, DjangoFilterBackend
from django_filters.widgets import CSVWidget
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from products.serializers import *


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny, ]


class CategoryCreateView(generics.CreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser, ]


class CategoryRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser, ]
    queryset = Category.objects.all()
    lookup_field = "slug"

    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        category.delete()
        return Response(
            {
                "success": True,
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Category successfully deleted",
            }
        )


class ProductFilterSet(FilterSet):
    tags = filters.CharFilter(distinct=True, widget=CSVWidget, method='filter_tags')
    name = filters.CharFilter()

    class Meta:
        model = Products
        fields = ['product_name', 'tags']

    def filter_tags(self, queryset, name, value):
        return queryset.filter(tags__name__in=value)


class ProductListView(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny, ]

    filter_backends = (DjangoFilterBackend,)
    filter_class = ProductFilterSet


class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser, ]


class ProductRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser, ]
    queryset = Products.objects.all()
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()
        return Response(
            {
                "success": True,
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Product successfully deleted",
            }
        )


class DiscountedProductsView(generics.ListAPIView):
    serializer_class = DiscountSerializer
    permission_classes = [AllowAny, ]
    queryset = Discount.objects.all()


class DiscountedProductCreateView(generics.CreateAPIView):
    serializer_class = DiscountSerializer
    permission_classes = [IsAdminUser, ]


class DiscountedProductRetUpDelView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DiscountSerializer
    permission_classes = [IsAdminUser, ]
    queryset = Discount.objects.all()
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()
        return Response(
            {
                "success": True,
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Discounted product successfully deleted",
            }
        )
