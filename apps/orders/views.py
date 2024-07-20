from django.db import transaction

from rest_framework import status
from rest_framework.generics import UpdateAPIView, ListAPIView, DestroyAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Orders, CartItem
from orders.serializers import (
    AddToCartSerializer, CartItemListSerializer,
    OrderCreateSerializer, UpdateCartItemSerializer, OrderListSerializer
)
from orders.permissions import IsOwnerOrStaff

from apps.accounts.serializers import UserAddressSerializer

class AddToCartView(APIView):
    serializer_class = AddToCartSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(
            data={
                "message": "Product added to cart.",
                "cart_item_id": serializer.instance.pk
            }, status=201
        )

    def get_serializer(self, **kwargs):
        """
        Requestda kelgan datani ishlash uchun serializer class ni
        kerakli parametrlarni o'tkazgan holda qaytaradi.
        Misol uchun `request` serializer class da ishlatiladimi? shu yerda
        qo'shib yuborish kerak
        """
        kwargs = self.get_serializer_context(**kwargs)
        return self.serializer_class(**kwargs)

    def get_serializer_context(self, **kwargs):
        """
        Serializer ga o'tkaziladigan asosiy context ni qaytaradi.
        """
        kwargs.update(
            {
                "request": self.request,
                "view": self,
                "user": self.request.user
            }
        )
        return kwargs


class UpdateUserCartItem(UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = UpdateCartItemSerializer
    lookup_field = 'product_id'

    def get_object(self):
        cart_item = get_object_or_404(
            self.queryset,
            user=self.request.user,
            product=self.kwargs.get(self.lookup_field)
        )
        return cart_item


class CartItemsListView(ListAPIView):
    queryset = CartItem.objects.select_related("product").prefetch_related("attributes").all()
    serializer_class = CartItemListSerializer
    pagination_class = None

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class CartItemDeleteView(DestroyAPIView):
    serializer_class = CartItemListSerializer
    queryset = CartItem.objects.all()

    def delete(self, request, *args, **kwargs):
        cart_item = get_object_or_404(
            self.queryset,
            user=request.user,
            pk=self.kwargs.get(self.lookup_field)
        )
        cart_item.delete()
        return Response(
            data={
                "success": True,
                "message": "Cart successfully deleted.",
            }, status=204
        )


class OrderCreateView(APIView):
    @transaction.atomic()
    def post(self, request):
        order_serializer = OrderCreateSerializer(data=request.data)
        address_serializer = UserAddressSerializer(data=request.data)

        if order_serializer.is_valid() and address_serializer.is_valid():
            address = address_serializer.save(user=request.user)
            order = order_serializer.save(user=request.user, address=address)

            return Response({
                'success': True,
                'message': 'Order created',
                'result': {
                    'order_id': order.id,
                    'total_price': order.total_price,
                    'status': order.status
                },
            })
        else:
            return Response(
                data={"message": "invalid_data", "errors": order_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    # def get_serializer(self, *args, **kwargs):
    #     """
    #     Return the serializer instance that should be used for validating and
    #     deserializing input, and for serializing output.
    #     """
    #     serializer_class = UserAddressSerializer
    #     kwargs['context'] = self.get_serializer_context()
    #     return serializer_class(*args, **kwargs)
    #
    # def get_serializer_context(self, **kwargs):
    #     return {'request': self.request}


class OrderListView(ListAPIView):
    serializer_class = OrderListSerializer
    queryset = Orders.objects.all()


class OrderCancelView(APIView):
    permission_classes = [IsOwnerOrStaff]

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Orders, id=kwargs.get('pk'))
        self.check_object_permissions(request, order)
        if order.status == Orders.Status.CREATED:
            order.status = Orders.Status.CANCELED
            order.save()
            return Response(data={'message': 'order cancelled'})

        return Response(
            data={'message': 'order cannot be cancelled'},
            status=status.HTTP_400_BAD_REQUEST
        )

