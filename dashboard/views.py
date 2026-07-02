from datetime import date
import json

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.shortcuts import render

from inventory.models import Product, Category
from customers.models import Customer
from suppliers.models import Supplier
from orders.models import (
    PurchaseOrder,
    SalesOrder,
    SalesItem,
)


@login_required
def home(request):

    # =====================================
    # Dashboard Statistics
    # =====================================

    total_products = Product.objects.count()

    total_categories = Category.objects.count()

    total_customers = Customer.objects.count()

    total_suppliers = Supplier.objects.count()

    total_purchase_orders = PurchaseOrder.objects.count()

    total_sales_orders = SalesOrder.objects.count()

    completed_sales = SalesOrder.objects.filter(
        status="Completed"
    ).count()

    received_orders = PurchaseOrder.objects.filter(
        status="Received"
    ).count()

    low_stock = Product.objects.filter(
        quantity__lte=10
    ).count()

    low_stock_products = Product.objects.filter(
        quantity__lte=10
    ).order_by("quantity")

    total_stock = sum(
        product.quantity
        for product in Product.objects.all()
    )

    inventory_value = sum(
        product.price * product.quantity
        for product in Product.objects.all()
    )

    total_revenue = sum(
        item.quantity * item.selling_price
        for item in SalesItem.objects.filter(
            sales_order__status="Completed"
        )
    )

    # =====================================
    # Recent Products
    # =====================================

    recent_products = Product.objects.order_by(
        "-created_at"
    )[:5]

    # =====================================
    # Recent Sales
    # =====================================

    recent_sales = SalesOrder.objects.select_related(
        "customer"
    ).order_by("-order_date")[:5]

    # =====================================
    # Upcoming Deliveries
    # =====================================

    today = date.today()

    upcoming_deliveries = PurchaseOrder.objects.filter(
        status="Pending",
        expected_delivery__gte=today,
    ).select_related(
        "supplier"
    ).order_by(
        "expected_delivery"
    )[:5]

    # =====================================
    # Category Chart
    # =====================================

    category_labels = []
    category_counts = []

    for category in Category.objects.all():

        category_labels.append(category.name)

        category_counts.append(

            Product.objects.filter(
                category=category
            ).count()

        )

    # =====================================
    # Stock Chart
    # =====================================

    stock_labels = []
    stock_values = []

    for product in Product.objects.all():

        stock_labels.append(product.name)

        stock_values.append(product.quantity)

    # =====================================
    # Monthly Sales Chart
    # =====================================

    monthly_sales = (

        SalesOrder.objects.filter(
            status="Completed"
        )

        .annotate(
            month=TruncMonth("order_date")
        )

        .values("month")

        .annotate(
            total=Count("id")
        )

        .order_by("month")

    )

    monthly_labels = []
    monthly_counts = []

    for sale in monthly_sales:

        monthly_labels.append(
            sale["month"].strftime("%b %Y")
        )

        monthly_counts.append(
            sale["total"]
        )

    # =====================================
    # Top Selling Products
    # =====================================

    top_products = (

        SalesItem.objects.values(
            "product__name"
        )

        .annotate(
            total_sold=Sum("quantity")
        )

        .order_by("-total_sold")[:5]

    )

    top_product_labels = []
    top_product_values = []

    for product in top_products:

        top_product_labels.append(
            product["product__name"]
        )

        top_product_values.append(
            product["total_sold"]
        )

    # =====================================
    # Context
    # =====================================

    context = {

        "today": today,

        "total_products": total_products,

        "total_categories": total_categories,

        "total_customers": total_customers,

        "total_suppliers": total_suppliers,

        "total_purchase_orders": total_purchase_orders,

        "total_sales_orders": total_sales_orders,

        "completed_sales": completed_sales,

        "received_orders": received_orders,

        "low_stock": low_stock,

        "low_stock_products": low_stock_products,

        "total_stock": total_stock,

        "inventory_value": inventory_value,

        "total_revenue": total_revenue,

        "recent_products": recent_products,

        "recent_sales": recent_sales,

        "upcoming_deliveries": upcoming_deliveries,

        "category_labels": json.dumps(category_labels),

        "category_counts": json.dumps(category_counts),

        "stock_labels": json.dumps(stock_labels),

        "stock_values": json.dumps(stock_values),

        "monthly_labels": json.dumps(monthly_labels),

        "monthly_counts": json.dumps(monthly_counts),

        "top_product_labels": json.dumps(
            top_product_labels
        ),

        "top_product_values": json.dumps(
            top_product_values
        ),

    }

    return render(
        request,
        "dashboard/home.html",
        context,
    )