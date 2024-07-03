from django.urls import path

from products.views import CategoryListView, CategoryCreateView, CategoryRetrieveUpdateDeleteView, ProductListView, \
    ProductCreateView, ProductRetrieveUpdateDeleteView, DiscountedProductsView, DiscountedProductCreateView, \
    DiscountedProductRetUpDelView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('category/create/', CategoryCreateView.as_view(), name='create_category'),
    path('category/<slug:slug>/', CategoryRetrieveUpdateDeleteView.as_view(), name='ret_up_del_category'),

    path('', ProductListView.as_view(), name='products'),
    path('create/', ProductCreateView.as_view(), name='create_products'),
    path('<int:pk>/', ProductRetrieveUpdateDeleteView.as_view(), name='ret_up_del_products'),

    path('discounted-products/', DiscountedProductsView.as_view(), name='discounted_products'),
    path('discounts-create/', DiscountedProductCreateView.as_view(), name='create_discounts'),
    path('discounts/<int:pk>/', DiscountedProductRetUpDelView.as_view(), name='ret_up_del_discounts'),
]
