from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):

    class Meta:

        model = Customer

        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "city",
            "address",
        ]

        widgets = {

            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter First Name"
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Last Name"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Email"
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Phone Number"
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter City"
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter Address"
                }
            ),

        }

    def clean_phone(self):

        phone = self.cleaned_data["phone"]

        if not phone.isdigit():

            raise forms.ValidationError(
                "Phone number must contain only digits."
            )

        if len(phone) != 10:

            raise forms.ValidationError(
                "Phone number must be exactly 10 digits."
            )

        return phone