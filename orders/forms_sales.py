from django import forms

from .models import SalesOrder, SalesItem


class SalesOrderForm(forms.ModelForm):

    class Meta:

        model = SalesOrder

        fields = [
            "customer",
            "status",
        ]

        widgets = {

            "customer": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

        }


class SalesItemForm(forms.ModelForm):

    class Meta:

        model = SalesItem

        fields = [
            "product",
            "quantity",
            "selling_price",
        ]

        widgets = {

            "product": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                }
            ),

            "selling_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                }
            ),

        }