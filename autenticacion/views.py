from django.shortcuts import render, redirect

from django.views.generic import View
from django.contrib.auth import login, logout, authenticate

from django.contrib import messages
from .forms import IniciarSesionForm, CustomAuthenticationForm
from django.templatetags.static import static
# from django.contrib.auth.forms import AuthenticationForm
from hojadevida.models import *
from .forms import *

# Create your views here.

def acceso_denegado(request):
    return render(request, "acceso_denegado.html")


class VRegistro(View):

    def get(self, request):
        form = IniciarSesionForm()
        eye_icon = request.build_absolute_uri(
        static("bs532/img/")
        )

        # user = User.objects.get(username="amolinacrn")
        try:
            user = User.objects.get(username="amolinacrn")
        except User.DoesNotExist:
            user = None
        # --- consultas ---

        foto_obj = FotosPersonale.objects.filter(
            nombre_usuario_id=user
        ).first()

    
        url_portada = ""
        

        if foto_obj:
            portada = getattr(foto_obj, "imagen_panel_izquierdo", None)
            
            if portada and portada.name:
                url_portada = request.build_absolute_uri(portada.url)

        context={
                "url_portada":url_portada,
                "form": form,
                 "eye_icon":eye_icon
                 }
        return render(request, "registro/registro.html", context)

    def post(self, request):

        form = IniciarSesionForm(request.POST)

        if form.is_valid():

            usuario = form.save()

            login(request, usuario)

            return redirect("home")

        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])

            return render(request, "registro/registro.html", {"form": form})


def cerrar_sesion(request):
    logout(request)

    return redirect("home")


def logear(request):

    try:
        user = User.objects.get(username="amolinacrn")
    except User.DoesNotExist:
        user = None
    # --- consultas ---

    foto_obj = FotosPersonale.objects.filter(
        nombre_usuario_id=user
    ).first()

    url_portada = ""  

    if foto_obj:
        portada = getattr(foto_obj, "imagen_panel_izquierdo", None)
        
        if portada and portada.name:
            url_portada = request.build_absolute_uri(portada.url)

    form = CustomAuthenticationForm()

    if request.method == "POST":
        form = CustomAuthenticationForm(request=request, data=request.POST or None)

        if form.is_valid():
            usuario = authenticate(
                username=request.POST["username"], password=request.POST["password"]
            )
            if usuario is not None:
                login(request, usuario)
                return redirect("home")

    eye_icon = request.build_absolute_uri(
        static("bs532/img/")
    )
    context={
            "url_portada":url_portada,
            "form": form,
            "eye_icon":eye_icon
            }
    

    return render(request, "login/login.html", context)


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

