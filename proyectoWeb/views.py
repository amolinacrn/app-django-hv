from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.templatetags.static import static
import base64
from hojadevida.models import *
from hojadevida.forms import *
from hojadevida.views import *
import os
import os.path
import unicodedata
import re

from django.shortcuts import render 

def es_acceso_hoja_vida(user):
    return user.is_authenticated and user.groups.filter(
        name="acceso-hoja-de-vida"
    ).exists()

def home(request):
    user = User.objects.get(username="amolinacrn")
    # --- consultas ---
    foto_obj = FotosPersonale.objects.filter(
        nombre_usuario=user
    ).only("foto_perfil").first()

    datos_personales = DatosPersonale.objects.filter(nombre_usuario=user)

    diplomas = TitulosAcademico.objects.filter(nombre_usuario=user)

    experiencias = ExperienciasLaborale.objects.filter(nombre_usuario=user)

    # --- icono ---
    eye_icon = request.build_absolute_uri(
        static("bs532/img/")
    )

    # # --- foto perfil segura ---
    foto_url_perfil = ""

    if foto_obj and foto_obj.foto_perfil:
        foto_url_perfil = request.build_absolute_uri(
            foto_obj.foto_perfil.url
        )

    # --- función helper para links ---
    def agregar_link(queryset, nombre):
        for i, obj in enumerate(queryset):
            obj.link = f"{nombre}_{i}"


    agregar_link(experiencias, "experiencias_laborales")
    agregar_link(diplomas, "titulo_obtenido")
    # --- contexto ---
    contexto = {
        "puede_ver_hv": es_acceso_hoja_vida(request.user),

        "eye_icon": eye_icon,

        "datos_personales": datos_personales,

        "estudios": diplomas,

        "experiencias_laborales": experiencias,

        "foto_perfil": foto_url_perfil,
    }
    return render(request, "plt-home.html", contexto)  #### cambio aqui: para vista principal



    
