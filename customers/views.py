from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from .models import Customer
from .forms import CustomerForm


def customer_list(request):

    customers = Customer.objects.all().order_by("-id")

    search = request.GET.get("search")

    if search:
        customers = customers.filter(
            first_name__icontains=search
        ) | Customer.objects.filter(
            last_name__icontains=search
        ) | Customer.objects.filter(
            email__icontains=search
        )

    paginator = Paginator(customers, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {

        "customers": page_obj,

        "page_obj": page_obj,

        "search": search,

    }

    return render(
        request,
        "customers/customer_list.html",
        context,
    )


def add_customer(request):

    if request.method == "POST":

        form = CustomerForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("customer_list")

    else:

        form = CustomerForm()

    return render(
        request,
        "customers/customer_form.html",
        {
            "form": form,
            "title": "Add Customer"
        },
    )


def edit_customer(request, pk):

    customer = get_object_or_404(Customer, id=pk)

    if request.method == "POST":

        form = CustomerForm(
            request.POST,
            instance=customer
        )

        if form.is_valid():

            form.save()

            return redirect("customer_list")

    else:

        form = CustomerForm(instance=customer)

    return render(
        request,
        "customers/customer_form.html",
        {
            "form": form,
            "title": "Edit Customer"
        },
    )


def delete_customer(request, pk):

    customer = get_object_or_404(Customer, id=pk)

    if request.method == "POST":

        customer.delete()

        return redirect("customer_list")

    return render(
        request,
        "customers/delete_customer.html",
        {
            "customer": customer
        },
    )