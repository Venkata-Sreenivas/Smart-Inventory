from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path(
        "admin/",
        admin.site.urls,
    ),

    # Home/Login
    path(
        "",
        include("accounts.urls"),
    ),

    # Dashboard
    path(
        "dashboard/",
        include("dashboard.urls"),
    ),

    # Inventory
    path(
        "inventory/",
        include("inventory.urls"),
    ),

    # Customers
    path(
        "customers/",
        include("customers.urls"),
    ),

    # Suppliers
    path(
        "suppliers/",
        include("suppliers.urls"),
    ),

    # Purchase Orders
    path(
        "orders/",
        include("orders.urls"),
    ),

    # Sales Orders
    path(
        "sales/",
        include("orders.sales_urls"),
    ),

    # Reports
    path(
        "reports/",
        include("reports.urls"),
    ),

    # Account URLs
    path(
        "accounts/",
        include("accounts.urls"),
    ),

]

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )