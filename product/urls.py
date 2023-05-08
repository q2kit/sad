from django.urls import path

from product.views import *

urlpatterns = [
    path("add/", add_book),
    path("get/", get_books),
]
