from django import forms
from django.forms import inlineformset_factory

from .models import PurchaseOrder, PurchaseItem


class PurchaseOrderForm(forms.ModelForm):

    class Meta:

        model = PurchaseOrder

        fields = [
            "supplier",
            "expected_delivery",
            "status",
            "remarks",
        ]

        widgets = {

            "supplier": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "expected_delivery": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),

        }


PurchaseItemFormSet = inlineformset_factory(

    PurchaseOrder,

    PurchaseItem,

    fields=[

        "product",

        "quantity",

        "purchase_price",

    ],

    extra=1,

    can_delete=True,

    widgets={

        "product": forms.Select(
            attrs={
                "class": "form-select product-select"
            }
        ),

        "quantity": forms.NumberInput(
            attrs={
                "class": "form-control quantity"
            }
        ),

        "purchase_price": forms.NumberInput(
            attrs={
                "class": "form-control price"
            }
        ),

    }

)