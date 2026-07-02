from django.http import HttpResponse

from reportlab.lib.units import inch

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)

from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
import json

from django.http import JsonResponse

from reportlab.lib import colors
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from .models import SalesOrder, SalesItem
from inventory.models import Product
from .forms_sales import (
    SalesOrderForm,
    SalesItemForm,
)


def sales_order_list(request):

    orders = SalesOrder.objects.select_related(
        "customer"
    ).order_by("-id")

    search = request.GET.get("search")

    if search:

        orders = orders.filter(
            customer__name__icontains=search
        )

    paginator = Paginator(orders, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(

        request,

        "orders/sales_order_list.html",

        {

            "orders": page_obj,

            "page_obj": page_obj,

            "search": search,

        },

    )


def add_sales_order(request):

    if request.method == "POST":

        form = SalesOrderForm(request.POST)

        if form.is_valid():

            order = form.save(commit=False)

            order.invoice_number = (
                f"INV-{SalesOrder.objects.count()+1:05d}"
            )

            order.save()

            return redirect(
                "sales_order_detail",
                pk=order.pk,
            )

    else:

        form = SalesOrderForm()

    return render(

        request,

        "orders/sales_order_form.html",

        {

            "form": form,

            "title": "New Sales Order",

        },

    )
    
from .models import SalesOrder, SalesItem


def sales_order_detail(request, pk):

    order = get_object_or_404(
        SalesOrder,
        pk=pk,
    )

    items = order.items.all()

    grand_total = sum(
        item.subtotal() for item in items
    )

    return render(

        request,

        "orders/sales_order_detail.html",

        {

            "order": order,

            "items": items,

            "grand_total": grand_total,

        },

    )
    
def add_sales_item(request, pk):

    order = get_object_or_404(
        SalesOrder,
        pk=pk,
    )

    if request.method == "POST":

        form = SalesItemForm(request.POST)

        if form.is_valid():

            product = form.cleaned_data["product"]

            if order.items.filter(product=product).exists():

                messages.error(
                    request,
                    "This product already exists in the sales order."
                )

            else:

                item = form.save(commit=False)

                item.sales_order = order

                item.save()

                messages.success(
                    request,
                    "Product added successfully."
                )

                return redirect(
                    "sales_order_detail",
                    pk=order.id,
                )
    
def complete_sale(request, pk):

    order = get_object_or_404(
        SalesOrder,
        pk=pk,
    )

    if order.stock_updated:

        messages.warning(
            request,
            "This sale has already been completed."
        )

        return redirect(
            "sales_order_detail",
            pk=pk,
        )

    # Check stock before updating
    for item in order.items.all():

        product = item.product

        if product.quantity < item.quantity:

            messages.error(
                request,
                f"Not enough stock available for {product.name}."
            )

            return redirect(
                "sales_order_detail",
                pk=pk,
            )

    # Deduct stock
    for item in order.items.all():

        product = item.product

        product.quantity -= item.quantity

        product.save()

    order.status = "Completed"
    order.stock_updated = True
    order.save()

    messages.success(
        request,
        "Sale completed successfully."
    )

    return redirect(
        "sales_order_detail",
        pk=pk,
    )
    
def edit_sales_item(request, pk):

    item = get_object_or_404(
        SalesItem,
        pk=pk,
    )

    if request.method == "POST":

        form = SalesItemForm(
            request.POST,
            instance=item,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Sales item updated successfully."
            )

            return redirect(
                "sales_order_detail",
                pk=item.sales_order.id,
            )

    else:

        form = SalesItemForm(
            instance=item,
        )

    return render(

        request,

        "orders/sales_item_form.html",

        {

            "form": form,

            "order": item.sales_order,

            "title": "Edit Sales Item",

        },

    )


def delete_sales_item(request, pk):

    item = get_object_or_404(
        SalesItem,
        pk=pk,
    )

    order_id = item.sales_order.id

    if request.method == "POST":

        item.delete()

        messages.success(
            request,
            "Sales item deleted successfully."
        )

        return redirect(
            "sales_order_detail",
            pk=order_id,
        )

    return render(

        request,

        "orders/delete_sales_item.html",

        {

            "item": item,

        },

    )
    
def sales_invoice_pdf(request, pk):

    order = get_object_or_404(
        SalesOrder,
        pk=pk,
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = f'attachment; filename="Invoice_{order.invoice_number}.pdf"'

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "<b>SMART INVENTORY MANAGEMENT</b>",
            styles["Title"],
        )
    )

    elements.append(Spacer(1, 0.25 * inch))

    elements.append(
        Paragraph(
            f"<b>Invoice:</b> {order.invoice_number}",
            styles["Normal"],
        )
    )

    elements.append(
        Paragraph(
            f"<b>Date:</b> {order.order_date}",
            styles["Normal"],
        )
    )

    elements.append(
        Paragraph(
            f"<b>Customer:</b> {order.customer}",
            styles["Normal"],
        )
    )

    elements.append(Spacer(1, 0.3 * inch))

    data = [

        [

            "Product",

            "Qty",

            "Price",

            "Subtotal",

        ]

    ]

    grand_total = 0

    for item in order.items.all():

        subtotal = item.subtotal()

        grand_total += subtotal

        data.append([

            item.product.name,

            item.quantity,

            f"₹ {item.selling_price}",

            f"₹ {subtotal}",

        ])

    data.append([

        "",

        "",

        "Grand Total",

        f"₹ {grand_total}",

    ])

    table = Table(data)

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("BACKGROUND", (0, 1), (-1, -2), colors.beige),

            ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

        ])

    )

    elements.append(table)

    elements.append(Spacer(1, 0.3 * inch))

    elements.append(

        Paragraph(

            "Thank you for your business!",

            styles["Heading2"],

        )

    )

    doc.build(elements)

    return response

def get_product_price(request, product_id):

    product = get_object_or_404(
        Product,
        pk=product_id,
    )

    return JsonResponse(
        {
            "price": float(product.price),
        }
    )
    
def sales_analytics(request):

    completed_orders = SalesOrder.objects.filter(
        status="Completed"
    )

    total_orders = SalesOrder.objects.count()

    completed = completed_orders.count()

    cancelled = SalesOrder.objects.filter(
        status="Cancelled"
    ).count()

    revenue = sum(
        item.subtotal()
        for item in SalesItem.objects.filter(
            sales_order__status="Completed"
        )
    )

    top_products = (

        SalesItem.objects.values(
            "product__name"
        )

        .annotate(
            total=Sum("quantity")
        )

        .order_by("-total")[:5]

    )

    labels = []

    values = []

    for p in top_products:

        labels.append(
            p["product__name"]
        )

        values.append(
            p["total"]
        )

    monthly = (

        SalesOrder.objects.filter(
            status="Completed"
        )

        .annotate(
            month=TruncMonth("order_date")
        )

        .values("month")

        .annotate(
            orders=Count("id")
        )

        .order_by("month")

    )

    month_labels = []

    month_values = []

    for m in monthly:

        month_labels.append(
            m["month"].strftime("%b %Y")
        )

        month_values.append(
            m["orders"]
        )

    return render(

        request,

        "orders/sales_analytics.html",

        {

            "total_orders": total_orders,

            "completed": completed,

            "cancelled": cancelled,

            "revenue": revenue,

            "labels": json.dumps(labels),

            "values": json.dumps(values),

            "month_labels": json.dumps(month_labels),

            "month_values": json.dumps(month_values),

        },

    )
    
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect


def cancel_sale(request, pk):

    order = get_object_or_404(
        SalesOrder,
        pk=pk,
    )

    if order.status != "Completed":

        messages.error(
            request,
            "Only completed sales can be cancelled."
        )

        return redirect(
            "sales_order_detail",
            pk=pk,
        )

    if not order.stock_updated:

        messages.error(
            request,
            "Stock has already been restored."
        )

        return redirect(
            "sales_order_detail",
            pk=pk,
        )

    for item in order.items.all():

        product = item.product

        product.quantity += item.quantity

        product.save()

    order.status = "Cancelled"

    order.stock_updated = False

    order.save()

    messages.success(
        request,
        "Sale cancelled and stock restored."
    )

    return redirect(
        "sales_order_detail",
        pk=pk,
    )