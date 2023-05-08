from django.urls import path

from order.views import *

urlpatterns = [
    path('add-to-cart/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('remove-from-cart/<int:book_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('order-history/', order_history, name='order_history'),
    path('order-detail/<int:order_id>/', order_detail, name='order_detail'),
]
