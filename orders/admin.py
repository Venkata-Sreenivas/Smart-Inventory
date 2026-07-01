from django.contrib import admin

from .models import (
    PurchaseOrder,
    PurchaseItem,
    SalesOrder,
    SalesItem,
)


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):

    list_display = (
        "order_number",
        "supplier",
        "status",
        "order_date",
    )

    search_fields = (
        "order_number",
        "supplier__company_name",
    )

    list_filter = (
        "status",
    )

    inlines = [PurchaseItemInline]


class SalesItemInline(admin.TabularInline):
    model = SalesItem
    extra = 1


@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):

    list_display = (
        "invoice_number",
        "customer",
        "status",
        "order_date",
    )

    search_fields = (
        "invoice_number",
        "customer__name",
    )

    list_filter = (
        "status",
    )

    inlines = [SalesItemInline]