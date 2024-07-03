from django.urls import path
from orders.views import AddToCartView, UpdateUserCartItem, CartItemsListView, OrderCreateView

urlpatterns = [
    path("add-to-cart/", AddToCartView.as_view(), name="add-to-cart"),
    path("update-cart-item/<int:product_id>/", UpdateUserCartItem.as_view(), name="update-cart-item"),
    path("cart-items/", CartItemsListView.as_view(), name='cart-items'),
    path('order-create/', OrderCreateView.as_view(), name='order-create'),
]
