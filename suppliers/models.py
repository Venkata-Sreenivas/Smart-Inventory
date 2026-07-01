from django.db import models


class Supplier(models.Model):

    company_name = models.CharField(
        max_length=200
    )

    contact_person = models.CharField(
        max_length=100
    )

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=15,
        unique=True
    )

    gst_number = models.CharField(
        max_length=30,
        unique=True
    )

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    country = models.CharField(
        max_length=100,
        default="India"
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["company_name"]

        verbose_name = "Supplier"

        verbose_name_plural = "Suppliers"

    def __str__(self):

        return self.company_name