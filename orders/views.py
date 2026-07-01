from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PurchaseOrderForm
from .models import PurchaseOrder


def purchase_order_list(request):

    orders = PurchaseOrder.objects.select_related(
        "supplier"
    ).order_by("-id")

    search = request.GET.get("search")

    if search:

        orders = orders.filter(
            supplier__company_name__icontains=search
        )

    paginator = Paginator(orders, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "orders/purchase_order_list.html",
        {
            "orders": page_obj,
            "page_obj": page_obj,
            "search": search,
        },
    )


def add_purchase_order(request):

    if request.method == "POST":

        form = PurchaseOrderForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("purchase_order_list")

    else:

        form = PurchaseOrderForm()

    return render(
        request,
        "orders/purchase_order_form.html",
        {
            "form": form,
            "title": "Add Purchase Order",
        },
    )