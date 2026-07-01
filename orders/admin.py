from django.contrib import admin

from .models import PurchaseOrder, PurchaseItem


class PurchaseItemInline(admin.TabularInline):

    model = PurchaseItem

    extra = 1


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):

    list_display = (

        "id",

        "supplier",

        "order_date",

        "status",

    )

    list_filter = (

        "status",

        "order_date",

    )

    inlines = [

        PurchaseItemInline

    ]