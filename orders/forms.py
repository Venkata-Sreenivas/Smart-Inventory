from django import forms

from .models import PurchaseOrder


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