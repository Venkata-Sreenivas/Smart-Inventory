from django.core.paginator import Paginator
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.contrib import messages

from .models import PurchaseOrder, PurchaseItem
from .forms import PurchaseOrderForm
from .forms_purchase import PurchaseItemForm


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

            order = form.save(commit=False)

            order.order_number = (
                f"PO-{PurchaseOrder.objects.count()+1:05d}"
            )

            order.save()

            return redirect(
                "purchase_order_detail",
                pk=order.pk,
            )

    else:

        form = PurchaseOrderForm()

    return render(
        request,
        "orders/purchase_order_form.html",
        {
            "form": form,
            "title": "New Purchase Order",
        },
    )


def purchase_order_detail(request, pk):

    order = get_object_or_404(
        PurchaseOrder,
        pk=pk,
    )

    # ---------- STOCK UPDATE ----------

    if (
        order.status == "Received"
        and not order.stock_updated
    ):

        for item in order.items.all():

            product = item.product

            product.quantity += item.quantity

            product.save()

        order.stock_updated = True

        order.save()

        messages.success(
            request,
            "Inventory updated successfully."
        )

    # ----------------------------------

    items = order.items.all()

    grand_total = sum(
        item.subtotal() for item in items
    )

    return render(
        request,
        "orders/purchase_order_detail.html",
        {
            "order": order,
            "items": items,
            "grand_total": grand_total,
        },
    )

from .forms_purchase import PurchaseItemForm
def add_purchase_item(request, pk):

    order = get_object_or_404(
        PurchaseOrder,
        pk=pk,
    )

    if request.method == "POST":

        form = PurchaseItemForm(request.POST)

        if form.is_valid():

            product = form.cleaned_data["product"]

            if order.items.filter(product=product).exists():

                messages.error(
                    request,
                    "This product already exists in the purchase order."
                )

            else:

                item = form.save(commit=False)

                item.purchase_order = order

                item.save()

                messages.success(
                    request,
                    "Product added successfully."
                )

                return redirect(
                    "purchase_order_detail",
                    pk=order.pk,
                )

    else:

        form = PurchaseItemForm()

    return render(
        request,
        "orders/purchase_item_form.html",
        {
            "form": form,
            "order": order,
            "title": "Add Purchase Item",
        },
    )
    
from django.contrib import messages

def receive_stock(request, pk):
    order = get_object_or_404(
        PurchaseOrder,
        pk=pk,
    )

    if order.stock_updated:

        messages.warning(
            request,
            "Stock has already been received."
        )

        return redirect(
            "purchase_order_detail",
            pk=pk,
        )

    for item in order.items.all():

        product = item.product

        product.quantity += item.quantity

        product.save()

    order.status = "Received"

    order.stock_updated = True

    order.save()

    messages.success(
        request,
        "Stock received successfully."
    )

    return redirect(
        "purchase_order_detail",
        pk=pk,
    )
    
def edit_purchase_order(request, pk):

    order = get_object_or_404(
        PurchaseOrder,
        pk=pk,
    )

    if request.method == "POST":

        form = PurchaseOrderForm(
            request.POST,
            instance=order,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Purchase Order updated successfully."
            )

            return redirect(
                "purchase_order_detail",
                pk=order.pk,
            )

    else:

        form = PurchaseOrderForm(
            instance=order
        )

    return render(

        request,

        "orders/purchase_order_form.html",

        {

            "form": form,

            "title": "Edit Purchase Order",

        },

    )


def delete_purchase_order(request, pk):

    order = get_object_or_404(
        PurchaseOrder,
        pk=pk,
    )

    if request.method == "POST":

        order.delete()

        messages.success(
            request,
            "Purchase Order deleted successfully."
        )

        return redirect(
            "purchase_order_list"
        )

    return render(

        request,

        "orders/delete_purchase_order.html",

        {

            "order": order,

        },

    )

def edit_purchase_item(request, pk):

    item = get_object_or_404(
        PurchaseItem,
        pk=pk,
    )

    if request.method == "POST":

        form = PurchaseItemForm(
            request.POST,
            instance=item,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Purchase Item updated successfully."
            )

            return redirect(
                "purchase_order_detail",
                pk=item.purchase_order.id,
            )

    else:

        form = PurchaseItemForm(
            instance=item,
        )

    return render(

        request,

        "orders/purchase_item_form.html",

        {

            "form": form,

            "order": item.purchase_order,

            "title": "Edit Purchase Item",

        },

    )
    
def delete_purchase_item(request, pk):

    item = get_object_or_404(
        PurchaseItem,
        pk=pk,
    )

    order_id = item.purchase_order.id

    if request.method == "POST":

        item.delete()

        messages.success(
            request,
            "Purchase Item deleted successfully."
        )

        return redirect(
            "purchase_order_detail",
            pk=order_id,
        )

    return render(

        request,

        "orders/delete_purchase_item.html",

        {

            "item": item,

        },

    )
    
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect


def cancel_purchase(request, pk):

    order = get_object_or_404(
        PurchaseOrder,
        pk=pk,
    )

    if order.status != "Received":

        messages.error(
            request,
            "Only received purchase orders can be cancelled."
        )

        return redirect(
            "purchase_order_detail",
            pk=pk,
        )

    if not order.stock_updated:

        messages.error(
            request,
            "Stock has already been rolled back."
        )

        return redirect(
            "purchase_order_detail",
            pk=pk,
        )

    # Reduce stock
    for item in order.items.all():

        product = item.product

        if product.quantity >= item.quantity:

            product.quantity -= item.quantity

            product.save()

    order.status = "Cancelled"

    order.stock_updated = False

    order.save()

    messages.success(
        request,
        "Purchase cancelled and stock rolled back."
    )

    return redirect(
        "purchase_order_detail",
        pk=pk,
    )