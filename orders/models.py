from django.db import models

from suppliers.models import Supplier
from customers.models import Customer
from inventory.models import Product


class PurchaseOrder(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Received", "Received"),
        ("Cancelled", "Cancelled"),
    ]

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE
    )

    order_number = models.CharField(
        max_length=20,
        unique=True
    )

    order_date = models.DateField(
        auto_now_add=True
    )

    expected_delivery = models.DateField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    stock_updated = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.order_number


class PurchaseItem(models.Model):

    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def subtotal(self):
        return self.quantity * self.purchase_price

    def __str__(self):
        return self.product.name


class SalesOrder(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    invoice_number = models.CharField(
        max_length=20,
        unique=True
    )

    order_date = models.DateField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    stock_updated = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.invoice_number


class SalesItem(models.Model):

    sales_order = models.ForeignKey(
        SalesOrder,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def subtotal(self):
        return self.quantity * self.selling_price

    def __str__(self):
        return self.product.name