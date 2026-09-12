from django.http import HttpResponse
from django.shortcuts import render
from .models import Requirement


def index(request):
    return render(request, "requerimientos/index.html")

def nuevo(request):

    if request.method == "POST":

        requester = request.POST["requester"]
        email = request.POST["email"]
        title = request.POST["title"]
        description = request.POST["description"]
        requirement_type = request.POST["requirement_type"]
        priority = request.POST["priority"]

        Requirement.objects.create(
            requester=requester,
            email=email,
            title=title,
            description=description,
            requirement_type=requirement_type,
            priority=priority
        )

    return render(request, "requerimientos/nuevo.html")

def lista_requerimientos(request):
    requirement = Requirement.objects.all()

    return render(
        request,
        "requerimientos/lista.html",
        {"requirements": requirement}
    )