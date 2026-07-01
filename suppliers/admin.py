from django.contrib import admin
from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):

    list_display = (
        "company_name",
        "contact_person",
        "phone",
        "city",
        "is_active",
    )

    search_fields = (
        "company_name",
        "contact_person",
        "email",
    )

    list_filter = (
        "city",
        "is_active",
    )

    ordering = (
        "company_name",
    )