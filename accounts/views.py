from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")

        password = request.POST.get("password")

        user = authenticate(

            request,

            username=username,

            password=password,

        )

        if user:

            login(request, user)

            return redirect("home")

        return render(

            request,

            "accounts/login.html",

            {

                "error": "Invalid username or password.",

            },

        )

    return render(

        request,

        "accounts/login.html",

    )


def logout_view(request):

    logout(request)

    return redirect("login")