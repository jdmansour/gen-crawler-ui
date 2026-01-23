from django.shortcuts import render, redirect


def index(request):
    # redirect to /api/
    return redirect("/api/")


def wlo_spa(request):
    return render(request, "wlo_spa.html")