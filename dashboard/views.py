from django.shortcuts import render
from inventory.models import Product, Category
from customers.models import Customer
import json


def home(request):

    total_products = Product.objects.count()

    total_categories = Category.objects.count()

    total_customers = Customer.objects.count()

    low_stock = Product.objects.filter(quantity__lte=10).count()

    inventory_value = sum(
        product.price * product.quantity
        for product in Product.objects.all()
    )

    recent_products = Product.objects.order_by("-created_at")[:5]

    category_labels = []
    category_counts = []

    for category in Category.objects.all():
        category_labels.append(category.name)
        category_counts.append(
            Product.objects.filter(category=category).count()
        )

    stock_labels = []
    stock_values = []

    for product in Product.objects.all():
        stock_labels.append(product.name)
        stock_values.append(product.quantity)

    context = {

        "total_products": total_products,

        "total_categories": total_categories,

        "total_customers": total_customers,

        "low_stock": low_stock,

        "inventory_value": inventory_value,

        "recent_products": recent_products,

        "category_labels": json.dumps(category_labels),

        "category_counts": json.dumps(category_counts),

        "stock_labels": json.dumps(stock_labels),

        "stock_values": json.dumps(stock_values),

    }

    return render(
        request,
        "dashboard/home.html",
        context
    )