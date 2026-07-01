from django.core.paginator import Paginator
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from .models import PurchaseOrder
from .forms import (
    PurchaseOrderForm,
    PurchaseItemFormSet,
)


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

            purchase_order = form.save(commit=False)

            purchase_order.order_number = (
                f"PO-{PurchaseOrder.objects.count()+1:05d}"
            )

            purchase_order.save()

            formset = PurchaseItemFormSet(
                request.POST,
                instance=purchase_order
            )

            if formset.is_valid():

                formset.save()

                return redirect("purchase_order_list")

        else:

            formset = PurchaseItemFormSet(request.POST)

    else:

        form = PurchaseOrderForm()

        formset = PurchaseItemFormSet()

    return render(
        request,
        "orders/purchase_order_form.html",
        {
            "form": form,
            "formset": formset,
            "title": "New Purchase Order",
        },
    )


def purchase_order_detail(request, pk):

    order = get_object_or_404(
        PurchaseOrder,
        pk=pk,
    )

    items = order.items.all()

    return render(
        request,
        "orders/purchase_order_detail.html",
        {
            "order": order,
            "items": items,
        },
    )