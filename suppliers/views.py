from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from .models import Supplier
from .forms import SupplierForm


def supplier_list(request):

    suppliers = Supplier.objects.all().order_by("-id")

    search = request.GET.get("search")

    if search:

        suppliers = suppliers.filter(
            company_name__icontains=search
        )

    paginator = Paginator(suppliers, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {

        "suppliers": page_obj,

        "page_obj": page_obj,

        "search": search,

    }

    return render(
        request,
        "suppliers/supplier_list.html",
        context
    )


def add_supplier(request):

    if request.method == "POST":

        form = SupplierForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("supplier_list")

    else:

        form = SupplierForm()

    return render(
        request,
        "suppliers/supplier_form.html",
        {
            "form": form,
            "title": "Add Supplier"
        }
    )


def edit_supplier(request, pk):

    supplier = get_object_or_404(
        Supplier,
        id=pk
    )

    if request.method == "POST":

        form = SupplierForm(
            request.POST,
            instance=supplier
        )

        if form.is_valid():

            form.save()

            return redirect("supplier_list")

    else:

        form = SupplierForm(
            instance=supplier
        )

    return render(
        request,
        "suppliers/supplier_form.html",
        {
            "form": form,
            "title": "Edit Supplier"
        }
    )


def delete_supplier(request, pk):

    supplier = get_object_or_404(
        Supplier,
        id=pk
    )

    if request.method == "POST":

        supplier.delete()

        return redirect("supplier_list")

    return render(
        request,
        "suppliers/delete_supplier.html",
        {
            "supplier": supplier
        }
    )