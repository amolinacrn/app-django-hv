from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.templatetags.static import static
from physimathcode.app_functions import * 
from proyectoWeb.models import MisPublicaciones
from proyectoWeb.forms import FormMisPublicaciones
from linkpreview import link_preview
from django.apps import apps
from hojadevida.models import *
from hojadevida.forms import *
from hojadevida.views import *
import os
import os.path
import unicodedata
import re
import base64

@login_required(login_url="/autenticacion/logear")
@user_passes_test(acceso_hoja_de_vida,login_url="/autenticacion/acceso-denegado/")
def delete_record_from_database(request, app_name, model_name, pk):
    el_modelo = apps.get_model(app_name, model_name)
    obj = get_object_or_404(el_modelo, pk=pk, nombre_usuario=request.user)
    obj.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))


def curr_hv(request):

    try:
        usuario_login = User.objects.get(username=request.user)
    except:
        usuario_login=None

    obj_usuario_login = FotosPersonale.objects.filter(
        nombre_usuario_id=usuario_login
    ).first()

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
    url_usuario_login=""

    if foto_obj:

        foto_perfil = getattr(foto_obj, "foto_perfil", None)

        if foto_perfil and foto_perfil.name:

            foto_url_perfil = request.build_absolute_uri(foto_perfil.url)
    

    if obj_usuario_login:

        obj_usuario_login=getattr(obj_usuario_login, "foto_perfil", None)

        if obj_usuario_login and obj_usuario_login.name:
            
            url_usuario_login = request.build_absolute_uri(obj_usuario_login.url)
         

    # --- función helper para links ---
    def agregar_link(queryset, nombre):
        for i, obj in enumerate(queryset):
            obj.link = f"{nombre}_{i}"

    agregar_link(participacion, "produccion_academica")
    agregar_link(experiencias, "experiencias_laborales")
    agregar_link(idiomas, "idioma_extrangero")
    agregar_link(diplomas, "titulo_obtenido")

    for objeto in list(competencias) + list(diplomas) + list(experiencias)+list(produccion):
        try:
            objeto.icono_url = request.build_absolute_uri(objeto.cargar_icono.url)
        except Exception:
            objeto.icono_url = None

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

        "foto_usuario_login":url_usuario_login,

    }

    return render(
        request,
        "curr-hv.html",
        contexto
    )


def funcion_home(rqst):
    try:
        usuario_login = User.objects.get(username=rqst.user)
    except:
        usuario_login=None

    try:
        user = User.objects.get(username="amolinacrn")
    except User.DoesNotExist:
        user = None
    # --- consultas ---

    foto_obj = FotosPersonale.objects.filter(
        nombre_usuario_id=user
    ).first()

    obj_usuario_login = FotosPersonale.objects.filter(
        nombre_usuario_id=usuario_login
    ).first()

    foto_url_perfil = ""
    url_portada = ""
    url_usuario_login=""
    

    if foto_obj:
        foto_perfil = getattr(foto_obj, "foto_perfil", None)
        portada = getattr(foto_obj, "imagen_de_portada", None)
        obj_usuario_login=getattr(obj_usuario_login, "foto_perfil", None)

        if foto_perfil and foto_perfil.name:
            foto_url_perfil = rqst.build_absolute_uri(foto_perfil.url)
         
        if portada and portada.name:
            url_portada = rqst.build_absolute_uri(portada.url)

        if obj_usuario_login and obj_usuario_login.name:
            url_usuario_login = rqst.build_absolute_uri(obj_usuario_login.url)
         

    datos_personales = DatosPersonale.objects.filter(nombre_usuario=user)

    diplomas = TitulosAcademico.objects.filter(nombre_usuario=user)

    experiencias = ExperienciasLaborale.objects.filter(nombre_usuario=user)

    tecnologias = CompetenciasTecnicasComputacionale.objects.filter(nombre_usuario=user)

    areas_de_interes = ProduccionAcademica.objects.filter(nombre_usuario=user)

    mis_publicaciones = MisPublicaciones.objects.all()

    # --- icono ---
    eye_icon_static = rqst.build_absolute_uri(
        static("bs532/img/")
    )

    # imagenes_carrusel = []

    # for i in range(1, 20):
    #     imagenes_carrusel.append(f"img{i}.jpg")


    for objeto in list(tecnologias) + list(diplomas) + list(experiencias)+list(areas_de_interes):
        try:
            objeto.icono_url = rqst.build_absolute_uri(objeto.cargar_icono.url)
        except Exception:
            objeto.icono_url = None
    

    # --- contexto ---
    contexto = {
        "eye_icon_static": eye_icon_static,

        "areas_de_interes":areas_de_interes,

        "tecnologias": tecnologias,

        "imagenesCarrusel":areas_de_interes,
        
        "puede_ver_hv": es_acceso_hoja_vida(rqst.user),

        "datos_personales": datos_personales,

        "estudios": diplomas,

        "experiencias_laborales": experiencias,

        "foto_perfil": foto_url_perfil,

        "foto_usuario_login":url_usuario_login,
        
        "url_portada": url_portada,

        "form_publicaciones": FormMisPublicaciones(),

        "las_publicaciones" : mis_publicaciones
    }

    return contexto
  
def home(request):
    contexto=funcion_home(request)
    
    return render(request, "plt-home.html", contexto)  #### cambio aqui: para vista principal

@login_required(login_url="/autenticacion/logear")
@user_passes_test(acceso_hoja_de_vida,login_url="/autenticacion/acceso-denegado/")
def home_post(request):
    contexto = funcion_home(request)
    form = FormMisPublicaciones()
    if request.method == "POST":

        form = FormMisPublicaciones(request.POST)
      
        if form.is_valid():
            obj = form.save(commit=False)
            obj.nombre_usuario_id = request.user.id
            try:

                # 1. Revisamos si es YouTube

                if es_youtube(obj.publicaciones_url):
                    
                    campo_id_video = obtener_id_youtube(obj.publicaciones_url)
                    
                    preview = obtener_preview_youtube(obj.publicaciones_url)
                                        
                    obj.titulo_publicacion = preview["titulo"]
                    obj.descripcion_publicacion = preview["descripcion"]
                    obj.imagen_publicacion = preview["imagen"]
                    obj.id_video = campo_id_video
                    obj.save()

                # 2. Si no es YouTube usamos link_preview

                else:
                    preview = link_preview(obj.publicaciones_url)
                    obj.titulo_publicacion = preview.title or ""
                    obj.descripcion_publicacion = preview.description or ""
                    obj.imagen_publicacion = preview.image or ""
                    obj.save()
            except:
                logger.exception("Error obteniendo datos de YouTube")
                contexto["form_preview"] = True
                contexto["advertencia_preview"]= "* No se pudo procesar el enlace."
              
    contexto["form"] = form

    return render(request, "plt-home.html", contexto)
    


    if request.method == "POST":

        url = request.POST.get("url")


        # Valores por defecto
        titulo = ""
        descripcion = ""
        imagen = ""


        try:

            # 1. Revisamos si es YouTube
            if es_youtube(url):

                preview = obtener_preview_youtube(url)

                titulo = preview["titulo"]
                descripcion = preview["descripcion"]
                imagen = preview["imagen"]


            # 2. Si no es YouTube usamos link_preview
            else:

                preview = link_preview(url)

                titulo = preview.title or ""
                descripcion = preview.description or ""
                imagen = preview.image or ""


        # Errores posibles de link_preview
        except (
            HTTPError,
            MaximumContentSizeError,
            RequestException
        ):

            titulo = "Vista previa no disponible"
            descripcion = ""
            imagen = ""


        # Guardamos siempre el registro
        bibliografia = FormMisPublicaciones(
            nombre_usuario_id=request.user.id,
            url=url,
            titulo=titulo,
            descripcion=descripcion,
            imagen=imagen,
        )

        bibliografia.save()


        return redirect("home")
