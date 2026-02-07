from django.shortcuts import render, redirect

from django.views.generic import View
from django.contrib.auth import login, logout, authenticate

from django.contrib import messages
from .forms import IniciarSesionForm, CustomAuthenticationForm

# from django.contrib.auth.forms import AuthenticationForm
from .forms import *


# Create your views here.


class VRegistro(View):

    def get(self, request):
        form = IniciarSesionForm()
        return render(request, "registro/registro.html", {"form": form})

    def post(self, request):

        form = IniciarSesionForm(request.POST)

        if form.is_valid():

            usuario = form.save()

            login(request, usuario)

            return redirect("hojadevida")

        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])

            return render(request, "registro/registro.html", {"form": form})


def cerrar_sesion(request):
    logout(request)

    return redirect("hojadevida")


def logear(request):

    form = CustomAuthenticationForm()

    if request.method == "POST":
        form = CustomAuthenticationForm(request=request, data=request.POST or None)

        if form.is_valid():
            usuario = authenticate(
                username=request.POST["username"], password=request.POST["password"]
            )
            if usuario is not None:
                login(request, usuario)
                return redirect("hojadevida")

    return render(request, "login/login.html", {"form": form})


class PermisosDocentesView(View):

    def get(self, request):

        if request.user.is_authenticated and request.user.is_superuser:
            form = PermisosParaDocentesForm()
            return render(request, "permisosdocentes.html", {"form": form})
        else:
            return redirect("logear")

    def post(self, request):

        if request.user.is_authenticated and request.user.is_superuser:

            form = PermisosParaDocentesForm(request.POST)

            if form.is_valid():

                form.save()

                print(request.POST, "############")

                return render(request, "permisosdocentes.html", {"form": form})

            else:
                return render(request, "permisosdocentes.html", {"form": form})
        else:
            return redirect("logear")
