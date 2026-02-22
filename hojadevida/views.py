from django.http import HttpResponse, HttpRequest
from django.template import Template, Context, loader
from django.contrib.auth.decorators import login_required
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

def slugify(texto: str) -> str:
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")
    texto = re.sub(r"[^a-z0-9\s]", "", texto)
    texto = re.sub(r"\s+", "_", texto)
    return texto

@login_required(login_url="/autenticacion/logear")
def delete_file_record(request, model_name, pk):
    Model = apps.get_model('hojadevida', model_name)
    obj = get_object_or_404(Model, pk=pk, nombre_usuario=request.user)
    obj.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url="/autenticacion/logear")
def phot_delete(request):
    deletfoto = FotosPersonale.objects.get(nombre_usuario_id=request.user.id)
    deletfoto.foto_perfil.delete()
    return redirect("get_datos")

@login_required(login_url="/autenticacion/logear")
def file_delete(request):
    deletfile = DatosPersonale.objects.get(nombre_usuario_id=request.user.id)
    deletfile.fotocopia_documento.delete()
    return redirect("get_datos")

@login_required(login_url="/autenticacion/logear")
def Menu_HV(request):

    if not request.user.is_authenticated:
        return redirect("login")

    user = request.user

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
        "datos_HV.html",
        contexto
    )

# def Menu_HV(request):
#     foto_perfil = FotosPersonale.objects.filter(nombre_usuario_id=request.user.id)
#     datos_personales = DatosPersonale.objects.filter(nombre_usuario_id=request.user.id)
#     diplomas_de_estudio = TitulosAcademico.objects.filter(nombre_usuario_id=request.user.id)
#     experiencias_laborales = ExperienciasLaborale.objects.filter(nombre_usuario_id=request.user.id)
#     idioma_extrangero = IdiomaExtrangero.objects.filter(nombre_usuario_id=request.user.id)
#     produccion_academica= ProduccionAcademica.objects.filter(nombre_usuario_id=request.user.id)
#     participacion_cientifica=ParticipacionCientifica.objects.filter(nombre_usuario_id=request.user.id)
#     competencias_tecnicas_computacionale=CompetenciasTecnicasComputacionale.objects.filter(nombre_usuario_id=request.user.id)

#     eye_icon = request.build_absolute_uri(static('bs532/img/'))
    
#     foto_url_perfil=""

#     foto=foto_perfil.first().foto_perfil

#     if foto_perfil and foto:
#         foto_url_perfil = request.build_absolute_uri(foto.url)
        
#     for e,qry_set in enumerate(participacion_cientifica):
#         qry_set.link = "produccion_academica_"+str(e)

#     for e,qry_set in enumerate(experiencias_laborales):
#         qry_set.link = "experiencias_laborales_"+str(e)

#     for e,qry_set in enumerate(idioma_extrangero):
#         qry_set.link = "idioma_extrangero_"+str(e)
    
#     for e,qry_set in enumerate(diplomas_de_estudio):
#         qry_set.link = "titulo_obtenido_"+str(e)

#     contexto={ 
#         'eye_icon': eye_icon,
#         "datos_personales":datos_personales,
#         "estudios": diplomas_de_estudio,
#         "experiencias_laborales":experiencias_laborales,
#         "foto_perfil":foto_url_perfil,
#         "idioma_extrangero": idioma_extrangero, 
#         "produccion_academica": produccion_academica,
#         "participacion_cientifica": participacion_cientifica,
#         "competencias_tecnicas_computacionale":competencias_tecnicas_computacionale,
#                 }
#     response = render(request,"datos_HV.html", contexto)
#     return response

@login_required(login_url="/autenticacion/logear")
def view_pdf_HV(request):
    
    foto_perfil = FotosPersonale.objects.filter(nombre_usuario_id=request.user.id)
    datos_personales = DatosPersonale.objects.filter(nombre_usuario_id=request.user.id)
    diplomas_de_estudio = TitulosAcademico.objects.filter(nombre_usuario_id=request.user.id)
    experiencias_laborales = ExperienciasLaborale.objects.filter(nombre_usuario_id=request.user.id)
    idioma_extrangero = IdiomaExtrangero.objects.filter(nombre_usuario_id=request.user.id)
    produccion_academica= ProduccionAcademica.objects.filter(nombre_usuario_id=request.user.id)
    participacion_cientifica=ParticipacionCientifica.objects.filter(nombre_usuario_id=request.user.id)
    competencias_tecnicas_computacionales=CompetenciasTecnicasComputacionale.objects.filter(nombre_usuario_id=request.user.id)

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
            # "modelo": TitulosAcademico,
            "certificado_pdf":"diploma_titulo",
            
        },
        "experiencias_laborales": {
            "queryset": experiencias_laborales,
            "certificado_pdf":"soportes_experincias_laborales",
        },
        "idioma_extrangero": {
            "queryset": idioma_extrangero,
            "certificado_pdf":"soporte_certificado_idioma",
        },
        "participacion_cientifica": {
            "queryset": participacion_cientifica,
            "certificado_pdf":"soportes_eventos_cientificos"
        },
        "competencias_tecnicas_computacionale": {
            "queryset": competencias_tecnicas_computacionales,
            "certificado_pdf":"soporte_competencia_computacional"
        },
    }

    documentacion_completa = list(chain(
        diplomas_de_estudio,
        experiencias_laborales,
        participacion_cientifica
    ))

    for _, info in  conjuto_modelos.items():
        if info["queryset"].count() != 0:
            for modelo in info["queryset"]:
                campo_pdf = info["certificado_pdf"]
                archivo = getattr(modelo, campo_pdf, None) if campo_pdf else None
                                    
                if archivo:
                    pdf_path = archivo.path
                    if pdf_path:
                        pages = convert_from_path(pdf_path, dpi=200)
                    imagenes_base64 = []
                    for page in pages:
                        buffer = BytesIO()
                        page.save(buffer, format="JPEG", quality=70)  # comprime
                        img_str = base64.b64encode(buffer.getvalue()).decode()
                        imagenes_base64.append(img_str)
                    matriz_imagenes_base64.append((imagenes_base64,modelo.link,archivo.url))

    contexto={ 
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
        "documentacion_completa": documentacion_completa
                }

    response = render_pdf_view("ver_pdf_hv.html", contexto)
    return response

@login_required(login_url="/autenticacion/logear")
def codigo_vistas_automaticas_post_hv(request,
                                      formulario_forms,
                                      models_model,
                                      plantilla_html, 
                                      sitweb,
                                      idq):

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

    if es_valido:
        obj = form.save()
        return (sitweb,idq,es_valido)

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
def Codigo_vistas_automaticas_get_hv(request,formulario_forms,
                                     models_model, documento_soporte, plantilla_html):
    expe_laboral = formulario_forms(
        current_user=request.user.id
    )
    queryset_dat = models_model.objects.filter(
        nombre_usuario_id=request.user.id
    )

    for objeto in queryset_dat:
        archivo_soporte = getattr(objeto, documento_soporte, None) if documento_soporte else None

        if archivo_soporte:
            try:
                objeto.documento_url = request.build_absolute_uri(
                    archivo_soporte.url
                   
                )
            except:
                objeto.documento_url = None
    
    contexto = {
        "form": expe_laboral,
        "querydat": queryset_dat,
    }

    return (plantilla_html, contexto)

class formDatPersonView:

    @login_required(login_url="/autenticacion/logear")
    def get_person_dat(request):

        var_estado = False

        datos_personales = DatosPersonalesForm(current_user=request.user.id)
        fperfiluser = FotosPersonalesForm()

        foto_url_perfil = ""
        path_foto_perfil = ""

        # Obtener objeto una sola vez
        foto_obj = FotosPersonale.objects.filter(
            nombre_usuario_id=request.user.id
        ).first()

        if foto_obj and getattr(foto_obj, "foto_perfil", None):

            if foto_obj.foto_perfil.name:
                foto_url_perfil = request.build_absolute_uri(
                    foto_obj.foto_perfil.url
                )

                path_foto_perfil = foto_obj.foto_perfil


        # Obtener datos personales
        name_doc_pdf = DatosPersonale.objects.filter(
            nombre_usuario_id=request.user.id
        ).first()

        if name_doc_pdf:

            archivo = getattr(name_doc_pdf, "fotocopia_documento", None) if "fotocopia_documento" else None

            if archivo and archivo.name:

                url_diploma = request.build_absolute_uri(archivo.url)

                name_doc_pdf.documento_diploma_url = url_diploma

                var_estado = True

        else:

            name_doc_pdf = "#"

        contexto = {
            "form": datos_personales,
            "fotoform": fperfiluser,
            "doc_name_PDF": name_doc_pdf,
            "estvar": var_estado,
            "foto_perfil": foto_url_perfil,
            "path_foto_perfil": path_foto_perfil
            }

        return render(request, "datos_personales.html", contexto)


    @login_required(login_url="/autenticacion/logear")
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

            return redirect("hojadevida")

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
    def get(self, request, id_diploma=None):
        if not request.user.is_authenticated:
            return redirect("logear")

        plantilla_html, contexto = Codigo_vistas_automaticas_get_hv(request,
                                                                    FormularioTitulosAcademicos,
                                                                    TitulosAcademico,
                                                                    "documento_soporte",
                                                                    "registro_formacion_academica.html")
        return render(request, plantilla_html, contexto)

       
    def post(self, request, id_diploma=None):

        if not request.user.is_authenticated:
            return redirect("logear")

   
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

    def get(self, request, id_explab=None):
        if not request.user.is_authenticated:
            return redirect("logear")

        plantilla_html, contexto = Codigo_vistas_automaticas_get_hv(request,
                                                                    FormExperienciaLaboral,
                                                                    ExperienciasLaborale,
                                                                    "documento_soporte",
                                                                    "registro_exp_laboral.html")
        return render(request, plantilla_html, contexto)

    def post(self, request, id_explab=0):

        if not request.user.is_authenticated:
            return redirect("logear")

   
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

    def get(self, request, id_pracad=None):

        if not request.user.is_authenticated:
            return redirect("logear")

        plantilla_html, contexto = Codigo_vistas_automaticas_get_hv(request,
                                                                    FormularioProduccionAcademica,
                                                                    ProduccionAcademica,
                                                                    None,
                                                                    "produccion_academica.html")
        return render(request, plantilla_html, contexto)


    def post(self, request, id_pracad=0):

        if not request.user.is_authenticated:
            return redirect("logear")

   
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
    def get(self, request, id_pcient=None):
        if not request.user.is_authenticated:
            return redirect("logear")
        plantilla_html, contexto = Codigo_vistas_automaticas_get_hv(request,
                                                                    FormularioParticipacionCientifica,
                                                                    ParticipacionCientifica,
                                                                    "documento_soporte",
                                                                    "participacion_cientifica.html")
        return render(request, plantilla_html, contexto)
    

    def post(self, request, id_pcient=0):
        if not request.user.is_authenticated:
            return redirect("logear")

   
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
    def get(self, request, id_comput=None):

        if not request.user.is_authenticated:
            return redirect("logear")
        plantilla_html, contexto = Codigo_vistas_automaticas_get_hv(request,
                                                                    CompetenciasTecnicasComputacionalesForm,
                                                                    CompetenciasTecnicasComputacionale,
                                                                    "documento_soporte",
                                                                    "competencias_computacionales.html")
        return render(request, plantilla_html, contexto)
    


    def post(self, request, id_comput=0):

        if not request.user.is_authenticated:
            return redirect("logear")

   
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
    def get(self, request, pasar_id = None):
        if not request.user.is_authenticated:
            return redirect("logear")
        plantilla_html, contexto = Codigo_vistas_automaticas_get_hv(request,
                                                                    FormularioIdiomaExtrangero,
                                                                    IdiomaExtrangero,
                                                                    "documento_soporte",
                                                                    "dominio_idiomas.html")
        return render(request, plantilla_html, contexto)

           
        
    def post(self, request, pasar_id=0):
        if not request.user.is_authenticated:
            return redirect("logear")
        
        plantilla, contexto, validacion_form = codigo_vistas_automaticas_post_hv(request,
                                                                FormularioIdiomaExtrangero,
                                                                IdiomaExtrangero,"dominio_idiomas.html",
                                                                "idioma_extangero",
                                                                pasar_id)
        if validacion_form:
            return redirect(plantilla, contexto)
        return render(request, plantilla,contexto)
            

        

