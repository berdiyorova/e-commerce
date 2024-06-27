from rest_framework import status
from rest_framework.generics import UpdateAPIView, ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.serializers import *


class AddToCartView(APIView):
    serializer_class = AddToCartSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        # # serializer qaytaradigan hamma exceptionlar
        # shu yerda clientga qaytariladi.
        serializer.is_valid(raise_exception=True)

        # # 1. serializer.save() serializer.create() methodga murojaat qiladi
        # #chunki serializer da hali `instance` attribute o'rnatilmagan,
        # #aks holda serializer.update(serializer.instance) method ni chaqirgan
        # #bo'lar edi
        # # 2. save method ni ichida ba'zi field larni o'rnatib ketish mumkin.:
        # #     >>> serializer.save(user=request.user)
        # # attributes va subtotallarni serializer class da hisob kitob qilamiz
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

    def get_serializer_context(self):
        """
        Serializer ga o'tkaziladigan asosiy context ni qaytaradi.
        """
        return {
            "request": self.request,
            "view": self,
            # example: AYtaylik serializerda user bilan ishlangan:
            "user": self.request.user
            # ...
        }


    # def post(self, request, *args, **kwargs):
    #     try:
    #         serializer = self.serializer_class(data=request.data)
    #         if not serializer.is_valid():
    #             print(serializer.errors)
    #             return Response(data={"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    #         data = serializer.validated_data
    #         attributes = data.get('attributes', [])
    #         subtotal = sum([AttributeValue.objects.get(id=attribute).price for attribute in attributes])
    #         item = CartItem.objects.create(
    #             user=request.user,
    #             quantity=data.get("quantity"),
    #             product=data.get("product"),
    #             subtotal=subtotal
    #         )
    #         return Response(data={"message": "Product added to cart item.", "result": {"cart_item_id": item.id}})

    #     except Products.DoesNotExist:
    #         return Response(data={"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


class UpdateUserCartItem(UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = UpdateCartItemSerializer
    lookup_field = 'product_id'

    def get_object(self):
        cart_item = self.queryset.get(user=self.request.user, product=self.kwargs.get(self.lookup_field))
        return cart_item


class CartItemsListView(ListAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemListSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class OrderCreateView(CreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderCreateSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                print(serializer.errors)
                return Response(data={"message": "invalid_data"}, status=status.HTTP_400_BAD_REQUEST)
            address = UserAddress.objects.get(id=serializer.validated_data.get("user_address"))
            cart_items = CartItem.objects.filter(id__in=serializer.validated_data.get("cart_items"))
            total_price = sum([item.subtotal for item in cart_items])
            order = Orders.objects.create(user=request.user, address=address, total_price=total_price)
            return Response(data={"message": "order_created", "result": {"order_id": order.id}})

        except Exception as e:
            return Response(data={"message": "error", "result": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
