from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import ProductForm
from .models import Product, Category


def product_list(request):

    products = Product.objects.all().order_by("-id")
    categories = Category.objects.all()

    search = request.GET.get("search")
    category = request.GET.get("category")

    if search:
        products = products.filter(name__icontains=search)

    if category:
        products = products.filter(category_id=category)

    paginator = Paginator(products, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {

        "products": page_obj,

        "page_obj": page_obj,

        "categories": categories,

        "search": search,

        "selected_category": category,

    }

    return render(
        request,
        "inventory/product_list.html",
        context,
    )


def add_product(request):

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect("product_list")

    else:

        form = ProductForm()

    return render(
        request,
        "inventory/product_form.html",
        {"form": form},
    )


def edit_product(request, pk):

    product = Product.objects.get(id=pk)

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product,
        )

        if form.is_valid():

            form.save()

            return redirect("product_list")

    else:

        form = ProductForm(instance=product)

    return render(
        request,
        "inventory/edit_product.html",
        {"form": form},
    )


def delete_product(request, pk):

    product = Product.objects.get(id=pk)

    if request.method == "POST":

        product.delete()

        return redirect("product_list")

    return render(
        request,
        "inventory/delete_product.html",
        {"product": product},
    )