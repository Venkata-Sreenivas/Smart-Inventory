from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.purchase_order_list,
        name="purchase_order_list"
    ),

    path(
        "add/",
        views.add_purchase_order,
        name="add_purchase_order"
    ),

]