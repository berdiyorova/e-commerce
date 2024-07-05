from django.urls import path
from orders.views import AddToCartView, UpdateUserCartItem, CartItemsListView, CartItemDeleteView, OrderCreateView

urlpatterns = [
    path("add-to-cart/", AddToCartView.as_view(), name="add-to-cart"),
    path("update-cart-item/<int:product_id>/", UpdateUserCartItem.as_view(), name="update-cart-item"),
    path("cart-items/", CartItemsListView.as_view(), name='cart-items'),
    path('delete-cart-item/<int:pk>/', CartItemDeleteView.as_view(), name='delete-cart-item'),
    path('order-create/', OrderCreateView.as_view(), name='order-create'),
]
