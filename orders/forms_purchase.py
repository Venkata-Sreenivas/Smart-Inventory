from django import forms
from .models import PurchaseItem


class PurchaseItemForm(forms.ModelForm):

    class Meta:

        model = PurchaseItem

        fields = [
            "product",
            "quantity",
            "purchase_price",
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
                    "min": 1
                }
            ),

            "purchase_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),

        }