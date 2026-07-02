from django.urls import path

from . import views

urlpatterns = [

    path(
        "",
        views.inventory_report,
        name="inventory_report",
    ),

    path(
        "sales/",
        views.sales_report,
        name="sales_report",
    ),

    path(
        "low-stock/",
        views.low_stock_report,
        name="low_stock_report",
    ),
    
    path(
        "inventory/export/",
        views.export_inventory_excel,
        name="export_inventory_excel",
    ),

]