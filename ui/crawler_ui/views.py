from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    return render(request, "index.html")


def wlo_spa(request):
    return render(request, "wlo_spa.html")