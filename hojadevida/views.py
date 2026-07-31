from django.http import HttpResponse, HttpRequest
from django.template import Template, Context, loader
from django.core.exceptions import FieldDoesNotExist
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.templatetags.static import static
from django.views.generic import View
from django.http import JsonResponse
from django.views.generic import CreateView
from django.contrib import messages
from itertools import chain
from pdf2image import convert_from_path
from io import BytesIO
import base64
from .utils_pdf import render_pdf_view
from django.conf import settings
from django.apps import apps
from .models import *
from .forms import *
import os
import os.path
import unicodedata
import re
from collections import defaultdict

def es_acceso_hoja_vida(user):
    return user.is_authenticated and user.groups.filter(
        name="acceso-hoja-de-vida"
    ).exists()

def obtener_url_absoluta(request, archivo):
    if not archivo:
        return None
    try:
        return request.build_absolute_uri(archivo.url)
    except Exception:
        return None

def acceso_hoja_de_vida(user):
    return user.groups.filter(name="acceso-hoja-de-vida").exists()

def slugify(texto: str) -> str:
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")
    texto = re.sub(r"[^a-z0-9\s]", "", texto)
    texto = re.sub(r"\s+", "_", texto)
    return texto

@login_required(login_url="/autenticacion/logear")
@user_passes_test(acceso_hoja_de_vida,login_url="/autenticacion/acceso-denegado/")
def delete_file_record(request, model_name, pk):
    Model = apps.get_model('hojadevida', model_name)
    obj = get_object_or_404(Model, pk=pk, nombre_usuario=request.user)
    obj.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

# @login_required(login_url="/autenticacion/logear")
# @user_passes_test(acceso_hoja_de_vida,login_url="/autenticacion/acceso-denegado/")
# def phot_delete(request):
#     deletfoto = FotosPersonale.objects.get(nombre_usuario_id=request.user.id)
#     deletfoto.foto_perfil.delete()
#     return redirect("get_datos")

@login_required(login_url="/autenticacion/logear")
@user_passes_test(acceso_hoja_de_vida,login_url="/autenticacion/acceso-denegado/")
def delete_image(request, campo):
    foto = FotosPersonale.objects.get(nombre_usuario=request.user)

    if campo in ["foto_perfil", "imagen_de_portada","imagen_panel_izquierdo"]:
        getattr(foto, campo).delete()

    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url="/autenticacion/logear")
@user_passes_test(acceso_hoja_de_vida,login_url="/autenticacion/acceso-denegado/")
def delete_imagen_icono_record(request, model_name, campo, pk ):
    Model = apps.get_model('hojadevida', model_name)
    foto = get_object_or_404(Model, pk=pk, nombre_usuario=request.user)

    if campo in ["cargar_icono"]:
        field = getattr(foto, campo)

        if field:
            field.delete(save=False)   # Elimina el archivo físico
            setattr(foto, campo, None) # O "" si el campo no acepta NULL
            foto.save(update_fields=[campo])

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url="/autenticacion/logear")
@user_passes_test(acceso_hoja_de_vida,login_url="/autenticacion/acceso-denegado/")
def file_delete(request):
    deletfile = DatosPersonale.objects.get(nombre_usuario_id=request.user.id)
    deletfile.fotocopia_documento.delete()
    return redirect("get_datos")

@login_required(login_url="/autenticacion/logear")
@user_passes_test(acceso_hoja_de_vida,login_url="/autenticacion/acceso-denegado/")
def funcion_Menu_HV(rqst):

    if not rqst.user.is_authenticated:
        return redirect("login")

    user = rqst.user

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
    eye_icon = rqst.build_absolute_uri(
        static("bs532/img/")
    )

    # --- foto perfil segura ---
    foto_url_perfil = ""

    if foto_obj and foto_obj.foto_perfil:
        foto_url_perfil = rqst.build_absolute_uri(
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

    try:
        usuario_login = User.objects.get(username=rqst.user)
    except:
        usuario_login=None

    obj_usuario_login = FotosPersonale.objects.filter(
        nombre_usuario_id=usuario_login
    ).first()

    url_usuario_login=""

    if obj_usuario_login:

        obj_usuario_login=getattr(obj_usuario_login, "foto_perfil", None)

        if obj_usuario_login and obj_usuario_login.name:
            
            url_usuario_login = rqst.build_absolute_uri(obj_usuario_login.url)

    # --- contexto ---
    contexto = {
        "puede_ver_hv": es_acceso_hoja_vida(rqst.user),

        "eye_icon": eye_icon,

        "datos_personales": datos_personales,

        "estudios": diplomas,

        "experiencias_laborales": experiencias,

        "foto_perfil": foto_url_perfil,

        "idioma_extrangero": idiomas,

        "produccion_academica": produccion,

        "participacion_cientifica": participacion,

        "competencias_tecnicas_computacionale": competencias,

        "foto_usuario_login":url_usuario_login

    }

    return contexto

@login_required(login_url="/autenticacion/logear")
@user_passes_test(acceso_hoja_de_vida,login_url="/autenticacion/acceso-denegado/")
def view_pdf_HV(request):

    foto_perfil = FotosPersonale.objects.filter(nombre_usuario_id=request.user.id)
    datos_personales = DatosPersonale.objects.filter(nombre_usuario_id=request.user.id)
    diplomas_de_estudio = TitulosAcademico.objects.filter(nombre_usuario_id=request.user.id)
    experiencias_laborales = ExperienciasLaborale.objects.filter(nombre_usuario_id=request.user.id)
    idioma_extrangero = IdiomaExtrangero.objects.filter(nombre_usuario_id=request.user.id)
    produccion_academica= ProduccionAcademica.objects.filter(nombre_usuario_id=request.user.id)
    participacion_cientifica=ParticipacionCientifica.objects.filter(nombre_usuario_id=request.user.id)
    competencias_tecnicas_computacionales=CompetenciasTecnicasComputacionale.objects.filter(nombre_usuario_id=request.user.id)
    imprimir_datos = ImprimirHojaDeVida.objects.filter(nombre_usuario_id=request.user.id).first()

    matriz_imagenes_base64 = []

    eye_icon = request.build_absolute_uri(static('bs532/img/'))

    foto_url_perfil=""

    if foto_perfil and foto_perfil.first().foto_perfil:
        foto_url_perfil = request.build_absolute_uri(foto_perfil.first().foto_perfil.url)

    for e,qry_set in enumerate(participacion_cientifica):
        qry_set.link = "produccion_academica_"+str(e)

    for e,qry_set in enumerate(experiencias_laborales):
        qry_set.link = "experiencias_laborales_"+str(e)

    for e,qry_set in enumerate(idioma_extrangero):
        qry_set.link = "idioma_extrangero_"+str(e)

    for e,qry_set in enumerate(diplomas_de_estudio):
        qry_set.link = "titulo_obtenido_"+str(e)

    for e,qry_set in enumerate(competencias_tecnicas_computacionales):
        qry_set.link = "titulo_obtenido_"+str(e)

    conjuto_modelos = {
        "diplomas_de_estudio": {
            "queryset": diplomas_de_estudio,
            "certificado_pdf":"documento_soporte",
            "imprimir_datos":imprimir_datos.imprimir_estudio if imprimir_datos else False,
        },
        "experiencias_laborales": {
            "queryset": experiencias_laborales,
            "certificado_pdf":"documento_soporte",
            "imprimir_datos":imprimir_datos.imprimir_experiencia if imprimir_datos else False,
        },
        "idioma_extrangero": {
            "queryset": idioma_extrangero,
            "certificado_pdf":"documento_soporte",
            "imprimir_datos":imprimir_datos.imprimir_idioma if imprimir_datos else False,
        },
        "participacion_cientifica": {
            "queryset": participacion_cientifica,
            "certificado_pdf":"documento_soporte",
            "imprimir_datos":imprimir_datos.imprimir_participacion if imprimir_datos else False,
        },
        "competencias_tecnicas_computacionale": {
            "queryset": competencias_tecnicas_computacionales,
            "certificado_pdf":"documento_soporte",
            "imprimir_datos":imprimir_datos.imprimir_tecnicas if imprimir_datos else False,
        },
    }

    for _, info in conjuto_modelos.items():
        imprimir_doc = info["imprimir_datos"]
        if info["queryset"].count() != 0 and imprimir_doc:
            for modelo in info["queryset"]:
                campo_pdf = info["certificado_pdf"]
                archivo = getattr(modelo, campo_pdf, None) if campo_pdf else None

                if not archivo:
                    continue

                pdf_path = archivo.path
                if not pdf_path:
                    continue

                pages = convert_from_path(
                    pdf_path,
                    dpi=200,
                    poppler_path="/usr/bin"
                )

                imagenes_base64 = []
                url_absoluta = request.build_absolute_uri(archivo.url)

                for page in pages:
                    buffer = BytesIO()
                    page.save(buffer, format="JPEG", quality=70)
                    img_str = base64.b64encode(buffer.getvalue()).decode()
                    imagenes_base64.append(img_str)

                matriz_imagenes_base64.append(
                    (imagenes_base64, modelo.link, url_absoluta, imprimir_doc)
                )
       
    contexto={
        "imprimir_datos":imprimir_datos,
        'eye_icon': eye_icon,
        "datos_personales": datos_personales,
        "estudios": diplomas_de_estudio,
        "experiencias_laborales":experiencias_laborales,
        "foto_perfil": foto_url_perfil,
        "idioma_extrangero": idioma_extrangero,
        "produccion_academica": produccion_academica,
        "participacion_cientifica": participacion_cientifica,
        "competencias_tecnicas_computacionale": competencias_tecnicas_computacionales,
        "matriz_imagenes_base64": matriz_imagenes_base64,
        "diplomas_de_estudio": diplomas_de_estudio,
        "experiencias_laborales":experiencias_laborales,
        "participacion_cientifica":participacion_cientifica
        }

    response = render_pdf_view("ver_pdf_hv.html", contexto)
    return response


@login_required(login_url="/autenticacion/logear")
@user_passes_test(acceso_hoja_de_vida,login_url="/autenticacion/acceso-denegado/")
def codigo_vistas_automaticas_post_hv(request,
                                      formulario_forms,
                                      models_model,
                                      plantilla_html,
                                      sitweb,
                                      idq,
                                      name_curso=False
                                      ):

    if idq and idq != 0:
        obj = get_object_or_404(
            models_model,
            id=idq,
            nombre_usuario=request.user
        )
        form = formulario_forms(
            request.POST,
            request.FILES,
            instance=obj
        )
    else:
        form = formulario_forms(
            request.POST,
            request.FILES,
            current_user=request.user.id
        )

    es_valido=form.is_valid()

    if name_curso and es_valido:
        codigo = form.cleaned_data["codigo_curso"]
        objet = form.save(commit=False)
        objet.nombre_curso = dict(form.fields["codigo_curso"].choices)[codigo]
        objet.save()
        return (sitweb,idq,es_valido)

    if es_valido:

        objet = form.save(commit=False)

        try:
            objet._meta.get_field("nit_empresa")
        except FieldDoesNotExist:
            pass

        else:

            nit = objet.nit_empresa

            experiencia = models_model.objects.filter(
                nombre_usuario_id=request.user.id,
                nit_empresa=nit,
                cargar_icono__isnull=False
            ).exclude(
                cargar_icono=""
            ).first()

            if experiencia:
                objet.cargar_icono = experiencia.cargar_icono
                print("hola mundo")

        objet.save()

        return (sitweb, idq, es_valido)
   
    queryset_dat = models_model.objects.filter(
        nombre_usuario=request.user
    )
    Contexto =  {
        "form": form,
        "querydat": queryset_dat,
        "id_actual": idq,
        "es_valido" : es_valido
    }

    return (plantilla_html, Contexto, es_valido)

@login_required(login_url="/autenticacion/logear")
@user_passes_test(acceso_hoja_de_vida,login_url="/autenticacion/acceso-denegado/")
def Codigo_vistas_automaticas_get_hv(request,formulario_forms,
                                     models_model, documento_soporte, plantilla_html):
    expe_laboral = formulario_forms(
        current_user=request.user.id
    )
    queryset_dat = models_model.objects.filter(
        nombre_usuario_id=request.user.id
    )

    for objeto in queryset_dat:

        objeto.documento_url = obtener_url_absoluta(
            request,
            getattr(objeto, documento_soporte, None) if documento_soporte else None
        )

        objeto.icono_url = obtener_url_absoluta(
            request,
            getattr(objeto, "cargar_icono", None)
        )

    eye_icon = request.build_absolute_uri(
        static("bs532/img/")
    )

    icono_media = request.build_absolute_uri(
        settings.MEDIA_URL + "files/img/imgHome/"
    )


    try:
        usuario_login = User.objects.get(username=request.user)
    except:
        usuario_login=None

    obj_usuario_login = FotosPersonale.objects.filter(
        nombre_usuario_id=usuario_login
    ).first()

    url_usuario_login=""

    if obj_usuario_login:

        obj_usuario_login=getattr(obj_usuario_login, "foto_perfil", None)

        if obj_usuario_login and obj_usuario_login.name:
            
            url_usuario_login = request.build_absolute_uri(obj_usuario_login.url)

    contexto = {
        "icono_media":icono_media,
        "eye_icon": eye_icon,
        "puede_ver_hv": es_acceso_hoja_vida(request.user),
        "form": expe_laboral,
        "querydat": queryset_dat,
        "foto_usuario_login":url_usuario_login,
    }

    return (plantilla_html, contexto)

class formDatPersonView:

    @login_required(login_url="/autenticacion/logear")
    @user_passes_test(acceso_hoja_de_vida,login_url="/autenticacion/acceso-denegado/")
    def get_person_dat(request):

        var_estado = False

        datos_personales = DatosPersonalesForm(current_user=request.user.id)
        fperfiluser = FotosPersonalesForm()

        foto_url_perfil = ""

        url_portada = ""

        url_portada_izquierda=""

        # Obtener objeto una sola vez
        foto_obj = FotosPersonale.objects.filter(
            nombre_usuario_id=request.user.id
        ).first()

        if foto_obj:
            foto_perfil = getattr(foto_obj, "foto_perfil", None)
            portada = getattr(foto_obj, "imagen_de_portada", None)
            portada_izquierda = getattr(foto_obj, "imagen_panel_izquierdo", None)

            if foto_perfil and foto_perfil.name:
                foto_url_perfil = request.build_absolute_uri(foto_perfil.url)


            if portada and portada.name:
                url_portada = request.build_absolute_uri(portada.url)


            if portada_izquierda and portada_izquierda.name:
                url_portada_izquierda = request.build_absolute_uri(portada_izquierda.url)

        # Obtener datos personales
        queryset_datos_personales = DatosPersonale.objects.filter(
            nombre_usuario_id=request.user.id
        )

        

        for file in queryset_datos_personales:
            archivo = getattr(file, "fotocopia_documento", None) if "fotocopia_documento" else None
            iconos_home = getattr(file, "cargar_icono", None) if "cargar_icono" else None

            if archivo and archivo.name:

                url_diploma = request.build_absolute_uri(archivo.url)

                queryset_datos_personales.documento_diploma_url = url_diploma

                var_estado = True

            if iconos_home and iconos_home.name:

                iconos_home_url = request.build_absolute_uri(iconos_home.url)

                queryset_datos_personales.url_iconos_home = iconos_home_url

        eye_icon = request.build_absolute_uri(
            static("bs532/img/")
        )

        contexto = {
            "portada_izquierda_url":url_portada_izquierda,
            "eye_icon": eye_icon,
            "qryset_foto_obj":foto_obj,
            "img_portada_url":url_portada ,
            "puede_ver_hv": es_acceso_hoja_vida(request.user),
            "form": datos_personales,
            "fotoform": fperfiluser,
            "doc_name_PDF": queryset_datos_personales,
            "estvar": var_estado,
            "foto_usuario_login": foto_url_perfil,
            "foto_perfil": foto_url_perfil,
            }

        return render(request, "datos_personales.html", contexto)


    @login_required(login_url="/autenticacion/logear")
    @user_passes_test(acceso_hoja_de_vida,login_url="/autenticacion/acceso-denegado/")
    def post_person_dat(request):

        if request.method != "POST":
            return render(request, "errores.html", {})

        var_estado = False

        fform = FotosPersonalesForm()

        # Obtener objeto si existe
        obj = DatosPersonale.objects.filter(
            nombre_usuario_id=request.user.id
        ).first()

        # verificar si ya tiene documento
        if obj and getattr(obj, "fotocopia_documento", None):

            if obj.fotocopia_documento.name:
                var_estado = True

        # crear formulario según exista o no el objeto
        if obj:

            form = DatosPersonalesForm(
                request.POST,
                request.FILES,
                instance=obj
            )

        else:

            form = DatosPersonalesForm(
                request.POST,
                request.FILES,
                current_user=request.user.id
            )


        if form.is_valid():

            form.save()

            return redirect("hojadevida", 0)

        # si el form no es válido
        contexto = {

            "form": form,
            "fotoform": fform,
            "doc_name_PDF": obj if obj else "",
            "estvar": var_estado,

        }

        return render(
            request,
            "datos_personales.html",
            contexto
        )

    @login_required(login_url="/autenticacion/logear")
    @user_passes_test(acceso_hoja_de_vida,login_url="/autenticacion/acceso-denegado/")
    def post_person_phot(request):

        if request.method != "POST":
            return render(request, "errores.html", {})

        obj = FotosPersonale.objects.filter(
            nombre_usuario_id=request.user.id
        ).first()

        form = FotosPersonalesForm(
            request.POST,
            request.FILES,
            instance=obj,
            current_user=request.user.id if not obj else None
        )

        if form.is_valid():

            form.save()

        return redirect("get_datos")


class FormacionAcademicaHV(View):

    def get(self, request, *args, **kwargs):
        id_diploma= kwargs.get("pk")
        if not request.user.is_authenticated:
            return redirect("logear")

        if not request.user.groups.filter(
            name="acceso-hoja-de-vida"
        ).exists():
            return redirect("/autenticacion/acceso-denegado/")

        plantilla_html, contexto = Codigo_vistas_automaticas_get_hv(request,
                                                                    FormularioTitulosAcademicos,
                                                                    TitulosAcademico,
                                                                    "documento_soporte",
                                                                    "registro_formacion_academica.html")
        return render(request, plantilla_html, contexto)


    def post(self, request, id_diploma):
       
        if not request.user.is_authenticated:
            return redirect("logear")

        if not request.user.groups.filter(
            name="acceso-hoja-de-vida"
        ).exists():
            return redirect("/autenticacion/acceso-denegado/")

        plantilla, contexto, validacion_form = codigo_vistas_automaticas_post_hv(request,
                                                                FormularioTitulosAcademicos,
                                                                TitulosAcademico,
                                                                "registro_formacion_academica.html",
                                                                "form_acad", #redirigir a esta vista,
                                                                id_diploma)

        if validacion_form:
            return redirect(plantilla, contexto)

        return render(request, plantilla,contexto)

class ExperienciaLaboralHV(View):

    def get(self, request, *args, **kwargs):
        id_explab = kwargs.get("pk")
        if not request.user.is_authenticated:
            return redirect("logear")

        if not request.user.groups.filter(
            name="acceso-hoja-de-vida"
        ).exists():
            return redirect("/autenticacion/acceso-denegado/")

        plantilla_html, contexto = Codigo_vistas_automaticas_get_hv(request,
                                                                    FormExperienciaLaboral,
                                                                    ExperienciasLaborale,
                                                                    "documento_soporte",
                                                                    "registro_exp_laboral.html")
        
        # nits_empresas = list(ExperienciasLaborale.objects.filter(
        #     nombre_usuario_id=request.user.id)
        #     )

        # diccionario_nit = {}

        # for obj in nits_empresas:

        #     if obj.cargar_icono:
        #         diccionario_nit[obj.nit_empresa] = obj.cargar_icono.url

        # for obj in nits_empresas:

        #     url_icono = diccionario_nit.get(obj.nit_empresa)

        #     if url_icono:
        #         obj.icono_url = request.build_absolute_uri(url_icono)
        #     else:
        #         obj.icono_url = ""

        # contexto["queryset_iconos"] = nits_empresas
        
        return render(request, plantilla_html, contexto)

    def post(self, request, id_explab=0):

        if not request.user.is_authenticated:
            return redirect("logear")

        if not request.user.groups.filter(
            name="acceso-hoja-de-vida"
        ).exists():
            return redirect("/autenticacion/acceso-denegado/")

        plantilla, contexto, validacion_form = codigo_vistas_automaticas_post_hv(request,
                                                                FormExperienciaLaboral,
                                                                ExperienciasLaborale,
                                                                "registro_exp_laboral.html",
                                                                "exp_laboral", #redirigir a esta vista,
                                                                id_explab)

        if validacion_form:
            return redirect(plantilla, contexto)

        return render(request, plantilla,contexto)

class ProduccionAcademicaHV(View):

    def get(self, request, *args,**kwargs):
        id_pracad= kwargs.get("pk")
        if not request.user.is_authenticated:
            return redirect("logear")
        if not request.user.groups.filter(
            name="acceso-hoja-de-vida"
        ).exists():
            return redirect("/autenticacion/acceso-denegado/")
        plantilla_html, contexto = Codigo_vistas_automaticas_get_hv(request,
                                                                    FormularioProduccionAcademica,
                                                                    ProduccionAcademica,
                                                                    "documento_soporte",
                                                                    "produccion_academica.html")
        return render(request, plantilla_html, contexto)


    def post(self, request, id_pracad=0):

        if not request.user.is_authenticated:
            return redirect("logear")

        if not request.user.groups.filter(
            name="acceso-hoja-de-vida"
        ).exists():
            return redirect("/autenticacion/acceso-denegado/")

        plantilla, contexto, validacion_form = codigo_vistas_automaticas_post_hv(request,
                                                                FormularioProduccionAcademica,
                                                                ProduccionAcademica,
                                                                "produccion_academica.html",
                                                                "prod_acad", #redirigir a esta vista,
                                                                id_pracad)

        if validacion_form:
            return redirect(plantilla, contexto)

        return render(request, plantilla,contexto)

class ParticipacionCientificaHV(View):

    def get(self, request, *args, **kwargs):
        id_pcient= kwargs.get("pk")
        if not request.user.is_authenticated:
            return redirect("logear")

        if not request.user.groups.filter(
            name="acceso-hoja-de-vida"
        ).exists():
            return redirect("/autenticacion/acceso-denegado/")

        plantilla_html, contexto = Codigo_vistas_automaticas_get_hv(request,
                                                                    FormularioParticipacionCientifica,
                                                                    ParticipacionCientifica,
                                                                    "documento_soporte",
                                                                    "participacion_cientifica.html")
        return render(request, plantilla_html, contexto)


    def post(self, request, id_pcient=0):
        if not request.user.is_authenticated:
            return redirect("logear")

        if not request.user.groups.filter(
            name="acceso-hoja-de-vida"
        ).exists():
            return redirect("/autenticacion/acceso-denegado/")


        plantilla, contexto, validacion_form = codigo_vistas_automaticas_post_hv(request,
                                                                FormularioParticipacionCientifica,
                                                                ParticipacionCientifica,
                                                                "participacion_cientifica.html",
                                                                "part_cient", #redirigir a esta vista,
                                                                id_pcient)

        if validacion_form:
            return redirect(plantilla, contexto)
        return render(request, plantilla,contexto)


class CompetenciasTecnicasComputacionalesHV(View):
    def get(self, request, *args, **kwargs):
        id_comput = kwargs.get("pk") 
        if not request.user.is_authenticated:
            return redirect("logear")

        if not request.user.groups.filter(
            name="acceso-hoja-de-vida"
        ).exists():
            return redirect("/autenticacion/acceso-denegado/")

        plantilla_html, contexto = Codigo_vistas_automaticas_get_hv(request,
                                                                    CompetenciasTecnicasComputacionalesForm,
                                                                    CompetenciasTecnicasComputacionale,
                                                                    "documento_soporte",
                                                                    "competencias_computacionales.html")
        return render(request, plantilla_html, contexto)



    def post(self, request, id_comput=0):

        if not request.user.is_authenticated:
            return redirect("logear")

        if not request.user.groups.filter(
            name="acceso-hoja-de-vida"
        ).exists():
            return redirect("/autenticacion/acceso-denegado/")

        plantilla, contexto, validacion_form = codigo_vistas_automaticas_post_hv(request,
                                                                CompetenciasTecnicasComputacionalesForm,
                                                                CompetenciasTecnicasComputacionale,
                                                                "competencias_computacionales.html",
                                                                "competencia_tecnica", #redirigir a esta vista,
                                                                id_comput)

        if validacion_form:
            return redirect(plantilla, contexto)
        return render(request, plantilla,contexto)


class IdiomaExtrangeroHV(View):
    def get(self, request, *args, **kwargs):
        pasar_id = kwargs.get("pk") 
        if not request.user.is_authenticated:
            return redirect("logear")
        if not request.user.groups.filter(
            name="acceso-hoja-de-vida"
        ).exists():
            return redirect("/autenticacion/acceso-denegado/")
        plantilla_html, contexto = Codigo_vistas_automaticas_get_hv(request,
                                                                    FormularioIdiomaExtrangero,
                                                                    IdiomaExtrangero,
                                                                    "documento_soporte",
                                                                    "dominio_idiomas.html")
        return render(request, plantilla_html, contexto)


    def post(self, request, pasar_id=0):
        if not request.user.is_authenticated:
            return redirect("logear")

        if not request.user.groups.filter(
            name="acceso-hoja-de-vida"
        ).exists():
            return redirect("/autenticacion/acceso-denegado/")

        plantilla, contexto, validacion_form = codigo_vistas_automaticas_post_hv(request,
                                                                FormularioIdiomaExtrangero,
                                                                IdiomaExtrangero,
                                                                "dominio_idiomas.html",
                                                                "idioma_extangero",
                                                                pasar_id)
        if validacion_form:
            return redirect(plantilla, contexto)
        return render(request, plantilla,contexto)


class CursosImpartidosHV(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if not request.user.is_authenticated:
            return redirect("logear")
        if not request.user.groups.filter(
            name="acceso-hoja-de-vida"
        ).exists():
            return redirect("/autenticacion/acceso-denegado/")
        plantilla_html, contexto = Codigo_vistas_automaticas_get_hv(request,
                                                                    FormCursosImpartidos,
                                                                    CursosImpartidos,
                                                                    None,
                                                                    "vista-docencia.html")
    
        mostrar_unidades = UnidadesCursosImpartidos.objects.filter(
            nombre_usuario_id=request.user.id
            )
        
        contexto["queryset_unidades"]=mostrar_unidades

        return render(request, plantilla_html, contexto)

    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect("logear")

        if not request.user.groups.filter(
            name="acceso-hoja-de-vida"
        ).exists():
            return redirect("/autenticacion/acceso-denegado/")

        plantilla, contexto, validacion_form = codigo_vistas_automaticas_post_hv(request,
                                                                FormCursosImpartidos,
                                                                CursosImpartidos,
                                                                "vista-docencia.html",
                                                                "cursos_impartidos",
                                                                pk)
        if validacion_form:
            return redirect(plantilla, contexto)
        return render(request, plantilla,contexto)

class UnidadesCursosImpartidosHV(View):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return redirect("logear")
        if not request.user.groups.filter(
            name="acceso-hoja-de-vida"
        ).exists():
            return redirect("/autenticacion/acceso-denegado/")
        plantilla_html, contexto = Codigo_vistas_automaticas_get_hv(request,
                                                                    FormUnidadesCursosImpartidos,
                                                                    UnidadesCursosImpartidos,
                                                                    None,
                                                                    "unidades-cursos-impartidos.html")
        
        contexto["id_actual"] = pk
        

        return render(request, plantilla_html, contexto)


    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect("logear")

        if not request.user.groups.filter(
            name="acceso-hoja-de-vida"
        ).exists():
            return redirect("/autenticacion/acceso-denegado/")

        plantilla, contexto, validacion_form = codigo_vistas_automaticas_post_hv(request,
                                                                FormUnidadesCursosImpartidos,
                                                                UnidadesCursosImpartidos,
                                                                "unidades-cursos-impartidos.html",
                                                                "unidades_cursos_impartidos",
                                                                pk)

        if validacion_form:
            return redirect("cursos_impartidos",0)
        return render(request, plantilla,contexto)


class CitasBibliograficasHV(View):
    def get(self, request, *args, **kwargs):
        pk=kwargs.get("pk")
        if not request.user.is_authenticated:
            return redirect("logear")
        if not request.user.groups.filter(
            name="acceso-hoja-de-vida"
        ).exists():
            return redirect("/autenticacion/acceso-denegado/")
        
        plantilla_html, contexto = Codigo_vistas_automaticas_get_hv(request,
                                                                    FormCitasBibliograficas,
                                                                    CitasBibliograficas,
                                                                    None,
                                                                    "citas-bibliograficas.html")

        return render(request, plantilla_html, contexto)

    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect("logear")

        if not request.user.groups.filter(
            name="acceso-hoja-de-vida"
        ).exists():
            return redirect("/autenticacion/acceso-denegado/")

        plantilla, contexto, validacion_form = codigo_vistas_automaticas_post_hv(request,
                                                                FormCitasBibliograficas,
                                                                CitasBibliograficas,
                                                                "citas-bibliograficas.html",
                                                                "bibliografia",
                                                                pk,
                                                                True)

        if validacion_form:
            return redirect(plantilla, contexto)
        return render(request, plantilla,contexto)


class ImprimirHojaDeVidaHV(View):
    def get(self, request, *args, **kwargs):
        pk=kwargs.get("pk")
        if not request.user.is_authenticated:
            return redirect("logear")
        if not request.user.groups.filter(
            name="acceso-hoja-de-vida"
        ).exists():
            return redirect("/autenticacion/acceso-denegado/")
        
        plantilla_html, contexto = Codigo_vistas_automaticas_get_hv(request,
                                                                    FormImprimirHojaDeVida,
                                                                    ImprimirHojaDeVida,
                                                                    None,
                                                                    "datos_HV.html")

        ImprimirHojaDeVida.objects.get_or_create(nombre_usuario=request.user)
        
        form_context=funcion_Menu_HV(request)
       
        form_context ["form_imprimir"]= contexto 
        

        return render(request, plantilla_html, form_context)

    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect("logear")

        if not request.user.groups.filter(
            name="acceso-hoja-de-vida"
        ).exists():
            return redirect("/autenticacion/acceso-denegado/")

        form_context=funcion_Menu_HV(request)

        plantilla, contexto, validacion_form = codigo_vistas_automaticas_post_hv(request,
                                                                FormImprimirHojaDeVida,
                                                                ImprimirHojaDeVida,
                                                                "datos_HV.html",
                                                                "hojadevida",
                                                                pk,
                                                                False)

        form_context ["form_imprimir"]= contexto       

        if validacion_form:
            return redirect(plantilla, contexto)
        return render(request, plantilla, form_context)
