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

def curr_hv(request):

    # user = User.objects.get(username="amolinacrn")
    try:
        user = User.objects.get(username="amolinacrn")
    except User.DoesNotExist:
        user = None

    # --- consultas ---
    foto_obj = FotosPersonale.objects.filter(
        nombre_usuario=user
    ).only("foto_perfil").first()

    datos_personales = DatosPersonale.objects.filter(nombre_usuario=user)

    diplomas = TitulosAcademico.objects.filter(nombre_usuario=user)

    experiencias = ExperienciasLaborale.objects.filter(nombre_usuario=user)

    idiomas = IdiomaExtrangero.objects.filter(nombre_usuario=user)

    produccion = ProduccionAcademica.objects.filter(nombre_usuario=user)

    participacion = ParticipacionCientifica.objects.filter(nombre_usuario=user)

    competencias = CompetenciasTecnicasComputacionale.objects.filter(
        nombre_usuario=user
    )

    # --- icono ---
    eye_icon = request.build_absolute_uri(
        static("bs532/img/")
    )

    # --- foto perfil segura ---
    foto_url_perfil = ""

    if foto_obj and foto_obj.foto_perfil:
        foto_url_perfil = request.build_absolute_uri(
            foto_obj.foto_perfil.url
        )

    # --- función helper para links ---
    def agregar_link(queryset, nombre):
        for i, obj in enumerate(queryset):
            obj.link = f"{nombre}_{i}"

    agregar_link(participacion, "produccion_academica")
    agregar_link(experiencias, "experiencias_laborales")
    agregar_link(idiomas, "idioma_extrangero")
    agregar_link(diplomas, "titulo_obtenido")

    # --- contexto ---
    contexto = {
        "puede_ver_hv": es_acceso_hoja_vida(request.user),
        "eye_icon": eye_icon,

        "datos_personales": datos_personales,

        "estudios": diplomas,

        "experiencias_laborales": experiencias,

        "foto_perfil": foto_url_perfil,

        "idioma_extrangero": idiomas,

        "produccion_academica": produccion,

        "participacion_cientifica": participacion,

        "competencias_tecnicas_computacionale": competencias,

    }

    return render(
        request,
        "curr-hv.html",
        contexto
    )



def home(request):
    # user = User.objects.get(username="amolinacrn")
    try:
        user = User.objects.get(username="amolinacrn")
    except User.DoesNotExist:
        user = None
    # --- consultas ---

    foto_obj = FotosPersonale.objects.filter(
        nombre_usuario_id=user
    ).first()

    foto_url_perfil = ""
    url_portada = ""
    

    if foto_obj:
        foto_perfil = getattr(foto_obj, "foto_perfil", None)
        portada = getattr(foto_obj, "imagen_de_portada", None)

        if foto_perfil and foto_perfil.name:
            foto_url_perfil = request.build_absolute_uri(foto_perfil.url)
         
        if portada and portada.name:
            url_portada = request.build_absolute_uri(portada.url)
         

    datos_personales = DatosPersonale.objects.filter(nombre_usuario=user)

    diplomas = TitulosAcademico.objects.filter(nombre_usuario=user)

    experiencias = ExperienciasLaborale.objects.filter(nombre_usuario=user)

    tecnologias = CompetenciasTecnicasComputacionale.objects.filter(nombre_usuario=user)

    areas_de_interes = ProduccionAcademica.objects.filter(nombre_usuario=user)

    # --- icono ---
    eye_icon = request.build_absolute_uri(
        static("bs532/img/")
    )

    imagenes_carrusel = []

    for i in range(1, 20):
        imagenes_carrusel.append(f"img{i}.jpg")

    for t in tecnologias:
        nombre = t.herramienta_tecnica

        if nombre == "C#":
            t.icono = "csharp"
        elif nombre == "C++":
            t.icono = "cpp"
        else:
            t.icono = nombre.lower().replace(" ", "")

    for t in areas_de_interes:
        nombre = t.linea_pesquisa
        t.icono = nombre.lower().replace(" ", "")
    

    # --- contexto ---
    contexto = {

        "areas_de_interes":areas_de_interes,

        "tecnologias": tecnologias,

        "imagenesCarrusel":imagenes_carrusel,
        
        "puede_ver_hv": es_acceso_hoja_vida(request.user),

        "eye_icon": eye_icon,

        "datos_personales": datos_personales,

        "estudios": diplomas,

        "experiencias_laborales": experiencias,

        "foto_perfil": foto_url_perfil,
        
        "url_portada": url_portada,
    }
    return render(request, "plt-home.html", contexto)  #### cambio aqui: para vista principal



    
