from django.shortcuts import render

from inventory.models import Product
from orders.models import SalesOrder

from django.http import HttpResponse
from openpyxl import Workbook

def inventory_report(request):

    products = Product.objects.select_related(
        "category"
    ).order_by("name")

    return render(
        request,
        "reports/inventory_report.html",
        {
            "products": products,
        },
    )


def sales_report(request):

    orders = SalesOrder.objects.select_related(
        "customer"
    ).order_by("-order_date")

    search = request.GET.get("search")

    if search:

        orders = orders.filter(
            customer__name__icontains=search
        )

    total_revenue = 0

    for order in orders:

        for item in order.items.all():

            total_revenue += item.subtotal()

    return render(

        request,

        "reports/sales_report.html",

        {

            "orders": orders,

            "total_revenue": total_revenue,

            "search": search,

        },

    )


def low_stock_report(request):

    products = Product.objects.filter(
        quantity__lte=10
    ).order_by("quantity")

    return render(

        request,

        "reports/low_stock_report.html",

        {

            "products": products,

        },

    )
    
def export_inventory_excel(request):

    workbook = Workbook()

    worksheet = workbook.active

    worksheet.title = "Inventory"

    worksheet.append([
        "ID",
        "Product",
        "Category",
        "Price",
        "Quantity",
    ])

    products = Product.objects.select_related(
        "category"
    )

    for product in products:

        worksheet.append([

            product.id,

            product.name,

            product.category.name,

            float(product.price),

            product.quantity,

        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = (
        'attachment; filename="Inventory_Report.xlsx"'
    )

    workbook.save(response)

    return response