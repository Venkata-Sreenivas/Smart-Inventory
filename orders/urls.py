from django.urls import path

from . import views

urlpatterns = [

    path(
        "",
        views.purchase_order_list,
        name="purchase_order_list",
    ),

    path(
        "add/",
        views.add_purchase_order,
        name="add_purchase_order",
    ),

    path(
        "<int:pk>/",
        views.purchase_order_detail,
        name="purchase_order_detail",
    ),

    path(
        "<int:pk>/edit/",
        views.edit_purchase_order,
        name="edit_purchase_order",
    ),

    path(
        "<int:pk>/delete/",
        views.delete_purchase_order,
        name="delete_purchase_order",
    ),

    path(
        "<int:pk>/items/add/",
        views.add_purchase_item,
        name="add_purchase_item",
    ),
    
    path(
        "items/<int:pk>/edit/",
        views.edit_purchase_item,
        name="edit_purchase_item",
    ),

    path(
        "items/<int:pk>/delete/",
        views.delete_purchase_item,
        name="delete_purchase_item",
    ),
    
    path(
        "<int:pk>/receive/",
        views.receive_stock,
        name="receive_stock",
    ),
    
    path(
        "<int:pk>/cancel/",
        views.cancel_purchase,
        name="cancel_purchase",
    ),
]