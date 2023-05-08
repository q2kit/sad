from django.urls import path

from user.views import *

urlpatterns = [
    path("register/admin/", register_admin),
    path("register/staff/", register_staff),
    path("register/customer/", register_customer),
    path("login/", login),
]
