from django.urls import path

from . import sales_views


urlpatterns = [

    path(
        "",
        sales_views.sales_order_list,
        name="sales_order_list",
    ),

    path(
        "add/",
        sales_views.add_sales_order,
        name="add_sales_order",
    ),

    path(
        "<int:pk>/",
        sales_views.sales_order_detail,
        name="sales_order_detail",
    ),

    path(
        "<int:pk>/items/add/",
        sales_views.add_sales_item,
        name="add_sales_item",
    ),

    path(
        "items/<int:pk>/edit/",
        sales_views.edit_sales_item,
        name="edit_sales_item",
    ),

    path(
        "items/<int:pk>/delete/",
        sales_views.delete_sales_item,
        name="delete_sales_item",
    ),

    path(
        "<int:pk>/complete/",
        sales_views.complete_sale,
        name="complete_sale",
    ),
    
    path(
        "<int:pk>/cancel/",
        sales_views.cancel_sale,
        name="cancel_sale",
    ),
    
    path(
        "<int:pk>/invoice/",
        sales_views.sales_invoice_pdf,
        name="sales_invoice_pdf",
    ),

    path(
        "product-price/<int:product_id>/",
        sales_views.get_product_price,
        name="get_product_price",
    ),

    path(
        "analytics/",
        sales_views.sales_analytics,
        name="sales_analytics",
    ),

]