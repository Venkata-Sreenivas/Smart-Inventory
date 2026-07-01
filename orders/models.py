from django.db import models

from suppliers.models import Supplier
from inventory.models import Product


class PurchaseOrder(models.Model):

    STATUS_CHOICES = [

        ("Pending", "Pending"),

        ("Received", "Received"),

        ("Cancelled", "Cancelled"),

    ]

    supplier = models.ForeignKey(

        Supplier,

        on_delete=models.CASCADE,

        related_name="purchase_orders"

    )

    order_date = models.DateField(

        auto_now_add=True

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

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    def __str__(self):

        return f"PO-{self.id}"


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