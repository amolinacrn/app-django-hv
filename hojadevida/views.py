from django.http import HttpResponse, HttpRequest
from django.template import Template, Context, loader
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.templatetags.static import static
from django.views.generic import View
from django.http import JsonResponse
from django.views.generic import CreateView
from django.contrib import messages
from pdf2image import convert_from_bytes
from itertools import chain
from pdf2image import convert_from_path
from supabase import create_client
from storages.backends.s3boto3 import S3Boto3Storage
from io import BytesIO
import requests
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


supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)

def get_signed_url(file_path):
    
    # file_path = request.GET.get("path")

    if not file_path:
        return JsonResponse({"error": "No existe el archivo"}, status=400)
    try:
        res = supabase.storage.from_("media").create_signed_url(file_path, 3600)
        return JsonResponse({"signed_url": res["signedURL"]})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def slugify(texto: str) -> str:
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")
    texto = re.sub(r"[^a-z0-9\s]", "", texto)
    texto = re.sub(r"\s+", "_", texto)
    return texto




@login_required(login_url="/autenticacion/logear")
def Menu_HV(request):
    if request.user.is_authenticated:

        foto_perfil = FotosPersonale.objects.filter(nombre_usuario_id=request.user.id)
        datos_personales = DatosPersonale.objects.filter(nombre_usuario_id=request.user.id)
        diplomas_de_estudio = TitulosAcademico.objects.filter(nombre_usuario_id=request.user.id)
        experiencias_laborales = ExperienciasLaborale.objects.filter(nombre_usuario_id=request.user.id)
        idioma_extrangero = IdiomaExtrangero.objects.filter(nombre_usuario_id=request.user.id)
        produccion_academica= ProduccionAcademica.objects.filter(nombre_usuario_id=request.user.id)
        participacion_cientifica=ParticipacionCientifica.objects.filter(nombre_usuario_id=request.user.id)
        competencias_tecnicas_computacionale=CompetenciasTecnicasComputacionale.objects.filter(nombre_usuario_id=request.user.id)

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

        contexto={ 
            'eye_icon': eye_icon,
            "datos_personales":datos_personales,
            "estudios": diplomas_de_estudio,
            "experiencias_laborales":experiencias_laborales,
            "foto_perfil":foto_url_perfil,
            "idioma_extrangero": idioma_extrangero, 
            "produccion_academica": produccion_academica,
            "participacion_cientifica": participacion_cientifica,
            "competencias_tecnicas_computacionale":competencias_tecnicas_computacionale,
                  }
        response = render(request,"datos_HV.html", contexto)
        return response
    else:
        return redirect("logear")

@login_required(login_url="/autenticacion/logear")
def delete_regist(request, id_file):
    deletfile = TitulosAcademico.objects.get(id=id_file)
    deletfile.delete()
    return redirect("form_acad", 0)

@login_required(login_url="/autenticacion/logear")
def view_pdf_HV(request):
    if request.user.is_authenticated:
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
                    archivo = getattr(modelo, campo_pdf)
                    if archivo and archivo.name:
                        path = archivo.name
                        result = supabase.storage.from_("media").create_signed_url(path, 3600)
                        pdf_url = result.get("signedURL") or result.get("signedUrl")
                        response = requests.get(pdf_url)
                        response.raise_for_status()
                        #  AQUÍ SE CONVIERTE EL PDF A PÁGINAS
                        pages = convert_from_bytes(response.content, dpi=200)
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
    else:
        return redirect("logear")

@login_required(login_url="/autenticacion/logear")
def delete_experience(request, id_file):
    deletfile = ExperienciasLaborale.objects.get(id=id_file)
    deletfile.delete()
    return redirect("exp_laboral", 0)

@login_required(login_url="/autenticacion/logear")
def delete_prod_acad(request, id_file):
    deletfile = ProduccionAcademica.objects.get(id=id_file)
    deletfile.delete()
    return redirect("prod_acad", 0)

def delete_file_record(request, model_name, pk):
    Model = apps.get_model('hojadevida', model_name)
    obj = get_object_or_404(Model, pk=pk)
    obj.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))
    # return redirect("get_datos")


class formDatPersonView:

    @login_required(login_url="/autenticacion/logear")
    def get_person_dat(request):
        var_estado = False
        datos_personales, fperfiluser = (
            DatosPersonalesForm(current_user=request.user.id),
            FotosPersonalesForm(),
        )

        
        url_absoluta = request.build_absolute_uri(settings.MEDIA_URL)
        
        foto_url_perfil=""

        foto_perfil = FotosPersonale.objects.filter(nombre_usuario_id=request.user.id)
        if foto_perfil and foto_perfil.first().foto_perfil:
                foto_url_perfil = request.build_absolute_uri(foto_perfil.first().foto_perfil.url)
                          

        try:
            
            name_doc_pdf = DatosPersonale.objects.get(nombre_usuario_id=request.user.id)
            
            if name_doc_pdf.fotocopia_documento.name != "":
                var_estado = True

            contexto = {
                "form": datos_personales,
                "fotoform": fperfiluser,
                "doc_name_PDF": name_doc_pdf,
                "estvar": var_estado,
                "url_absoluta":url_absoluta,
                "foto_perfil":foto_url_perfil
            }
        except:
            contexto = {
                "form": datos_personales,
                "fotoform": fperfiluser,
                "doc_name_PDF": "#",
                "estvar": var_estado,
                "foto_perfil":foto_url_perfil
            }

        return render(request, "datos_personales.html", contexto)

    @login_required(login_url="/autenticacion/logear")
    def post_person_dat(request):
        var_estado = False
        (forms, fform) = (
            DatosPersonalesForm(),
            FotosPersonalesForm(),
        )

        try:

            name_doc_pdf = DatosPersonale.objects.get(nombre_usuario_id=request.user.id)

            if name_doc_pdf.fotocopia_documento.name != "":
                var_estado = True

            else:
                pass

            if request.method == "POST":

                forms = DatosPersonalesForm(
                    request.POST, request.FILES, instance=name_doc_pdf
                )

                if forms.is_valid():
                    forms.save()
                    return redirect("hojadevida")
                else:

                    return render(
                        request,
                        "datos_personales.html",
                        {
                            "form": forms,
                            "fotoform": fform,
                            "doc_name_PDF": name_doc_pdf,
                            "estvar": var_estado,
                        },
                    )

            else:
                return render(request, "errores.html", {"form": forms.errors})
        except:
            if request.method == "POST":

                forms = DatosPersonalesForm(
                    request.POST, request.FILES, current_user=request.user.id
                )

                if forms.is_valid():
                    forms.save()
                    return redirect("hojadevida")
                else:
                    return render(
                        request,
                        "datos_personales.html",
                        {
                            "form": forms,
                            "fotoform": fform,
                            "doc_name_PDF": "",
                            "estvar": var_estado,
                        },
                    )
            else:
                return render(request, "errores.html", {"form": forms.errors})

    @login_required(login_url="/autenticacion/logear")
    def post_person_phot(request):
        forms = FotosPersonalesForm()

        try:
            objdb = FotosPersonale.objects.get(nombre_usuario_id=request.user.id)
            if request.method == "POST":
                forms = FotosPersonalesForm(request.POST, request.FILES, instance=objdb)
                if forms.is_valid():
                    forms.save()
                    return redirect("get_datos")
                else:
                    return redirect("get_datos")
            else:
                return render(request, "errores.html", {"form": forms.errors})
        except:
            if request.method == "POST":
                forms = FotosPersonalesForm(
                    request.POST, request.FILES, current_user=request.user.id
                )
                if forms.is_valid():
                    forms.save()
                    return redirect("get_datos")
                else:
                    return redirect("get_datos")
            else:
                return render(request, "errores.html", {"form": forms.errors})

    @login_required(login_url="/autenticacion/logear")
    def phot_delete(request):
        deletfoto = FotosPersonale.objects.get(nombre_usuario_id=request.user.id)
        deletfoto.foto_perfil.delete()
        return redirect("get_datos")
    

    def file_delete(request):
        deletfile = DatosPersonale.objects.get(nombre_usuario_id=request.user.id)
        deletfile.fotocopia_documento.delete()
        return redirect("get_datos")

    @login_required(login_url="/autenticacion/logear")
    def get_imgfoto(_request):

        try:
            objdb = FotosPersonale.objects.get(nombre_usuario_id=_request.user.id)
            imgusuario = [
                {
                    "fotoperfil": objdb.foto_perfil.name,
                    "nameimg": objdb.foto_perfil.name.split("/")[3],
                }
            ]

            Context = {"img_usuario": imgusuario}

            return JsonResponse(Context)

        except:
            Context = {"img_usuario": []}
            return JsonResponse(Context)

    @login_required(login_url="/autenticacion/logear")
    def getjs_file(_request):
        try:
            dbfile = DatosPersonale.objects.get(nombre_usuario_id=_request.user.id)

            pathfile = [
                {
                    "filepdf": dbfile.fotocopia_documento.name.split("/")[3],
                }
            ]

            Context = {"file_usuario": pathfile}
            return JsonResponse(Context)
        except:
            Context = {"file_usuario": []}
            return JsonResponse(Context)


class FormacionAcademicaHV(View):

    def get(self, request, id_diploma):
        if request.user.is_authenticated:
            formacion_academica = FormularioTitulosAcademicos(
                current_user=request.user.id
            )
            queryset_dat = TitulosAcademico.objects.filter(
                nombre_usuario_id=request.user.id
            )

            
            for objeto in queryset_dat:
                if objeto and objeto.diploma_titulo and objeto.diploma_titulo.url:
                    archivo_url = objeto.diploma_titulo.url
                    url_diploma = request.build_absolute_uri(archivo_url)  
                    objeto.documento_diploma_url = url_diploma
                  

            contexto = {
                "form": formacion_academica,
                "querydat": queryset_dat,
            }
            return render(request, "registro_formacion_academica.html", contexto)

        else:
            return redirect("logear")

    def post(self, request, id_diploma=0):
        if request.user.is_authenticated:
            id_actual = id_diploma
            varcondicioonal = False
            formacion_academica = FormularioTitulosAcademicos()

            if request.method == "POST":
                try:
                    edit_soporte = TitulosAcademico.objects.get(id=id_diploma)
                   
                    formacion_academica = FormularioTitulosAcademicos(
                        request.POST, request.FILES, instance=edit_soporte
                    )
                    id_diploma = 0
                except:
                    formacion_academica = FormularioTitulosAcademicos(
                        request.POST, request.FILES, current_user=request.user.id
                    )

                if formacion_academica.is_valid():
                    formacion_academica.save()
                    queryset_dat = TitulosAcademico.objects.filter(
                        nombre_usuario_id=request.user.id
                    )
                    
                    if id_diploma == 0:
                        return redirect("form_acad", id_diploma)

                    else:
                        contexto = {
                            "form": formacion_academica,
                            "querydat": queryset_dat,
                        }
                        return render(
                            request, "registro_formacion_academica.html", contexto
                        )
                else:
                    varcondicioonal = True
                    contexto = {
                        "form": formacion_academica,
                        "errform": varcondicioonal,
                        "id_actual": id_actual,
                    }
                    return render(
                        request, "registro_formacion_academica.html", contexto
                    )
            else:
                return render(
                    request, "errores.html", {"form": formacion_academica.errors}
                )
        else:
            return redirect("logear")



class ExperienciaLaboralHV(View):

    def get(self, request, id_explab=0):
        if not request.user.is_authenticated:
            return redirect("logear")

        expe_laboral = FormExperienciaLaboral(current_user=request.user.id)
        queryset_dat = ExperienciasLaborale.objects.filter(
            nombre_usuario_id=request.user.id
        )

        url_absoluta = request.build_absolute_uri(settings.MEDIA_URL)
        
        for e in queryset_dat:
                e.documento_url = url_absoluta

        contexto = {
            "form": expe_laboral,
            "querydat": queryset_dat,
        }
        return render(request, "registro_exp_laboral.html", contexto)

    def post(self, request, id_explab=0):
        if not request.user.is_authenticated:
            return redirect("logear")

        id_actual = id_explab
        varcond = False
        expe_laboral = FormExperienciaLaboral()

        if request.method == "POST":
            try:
                edit_soporte = ExperienciasLaborale.objects.get(id=id_explab)
                expe_laboral = FormExperienciaLaboral(
                    request.POST, request.FILES, instance=edit_soporte
                )
                id_explab = 0
                # print(request.FILES["soportes_experincias_laborales"])
            except:
                expe_laboral = FormExperienciaLaboral(
                    request.POST, request.FILES, current_user=request.user.id
                )

            if expe_laboral.is_valid():
                expe_laboral.save()
                queryset_dat = ExperienciasLaborale.objects.filter(
                    nombre_usuario_id=request.user.id
                )
                if id_explab == 0:
                    return redirect("exp_laboral", id_explab)

                else:
                    contexto = {
                        "form": expe_laboral,
                        "querydat": queryset_dat,
                    }
                    return render(request, "registro_exp_laboral.html", contexto)
            else:
                varcond = True
                contexto = {
                    "form": expe_laboral,
                    "errform": varcond,
                    "id_actual": id_actual,
                }
                return render(request, "registro_exp_laboral.html", contexto)
        else:
            return render(request, "errores.html", {"form": expe_laboral.errors})


class ProduccionAcademicaHV(View):

    def get(self, request, id_pracad):
        if request.user.is_authenticated:
            expe_laboral = FormularioProduccionAcademica(current_user=request.user.id)
            queryset_dat = ProduccionAcademica.objects.filter(
                nombre_usuario_id=request.user.id
            )

            contexto = {
                "form": expe_laboral,
                "querydat": queryset_dat,
            }
            return render(request, "produccion_academica.html", contexto)

        else:
            return redirect("logear")

    def post(self, request, id_pracad=0):
        if request.user.is_authenticated:
            id_actual = id_pracad
            varcond = False
            expe_laboral = FormularioProduccionAcademica()

            if request.method == "POST":
                try:
                    edit_soporte = ProduccionAcademica.objects.get(id=id_pracad)
                    expe_laboral = FormularioProduccionAcademica(
                        request.POST, request.FILES, instance=edit_soporte
                    )
                    id_pracad = 0
                    # print(request.FILES["soportes_experincias_laborales"])
                except:
                    expe_laboral = FormularioProduccionAcademica(
                        request.POST, request.FILES, current_user=request.user.id
                    )

                if expe_laboral.is_valid():
                    expe_laboral.save()
                    queryset_dat = ProduccionAcademica.objects.filter(
                        nombre_usuario_id=request.user.id
                    )
                    if id_pracad == 0:
                        return redirect("prod_acad", id_pracad)

                    else:
                        contexto = {
                            "form": expe_laboral,
                            "querydat": queryset_dat,
                        }
                        return render(request, "produccion_academica.html", contexto)
                else:
                    varcond = True
                    contexto = {
                        "form": expe_laboral,
                        "errform": varcond,
                        "id_actual": id_actual,
                    }
                    return render(request, "produccion_academica.html", contexto)
            else:
                return render(request, "errores.html", {"form": expe_laboral.errors})
        else:
            return redirect("logear")


class ParticipacionCientificaHV(View):

    def get(self, request, id_pcient=0):
        if request.user.is_authenticated:
            expe_laboral = FormularioParticipacionCientifica(
                current_user=request.user.id
            )
            queryset_dat = ParticipacionCientifica.objects.filter(
                nombre_usuario_id=request.user.id
            )

            url_absoluta = request.build_absolute_uri(settings.MEDIA_URL)

            for e in queryset_dat:
                e.documento_url = url_absoluta

            contexto = {
                "form": expe_laboral,
                "querydat": queryset_dat,
            }
            return render(request, "participacion_cientifica.html", contexto)

        else:
            return redirect("logear")

    def post(self, request, id_pcient=0):
        if request.user.is_authenticated:
            id_actual = id_pcient
            varcond = False
            expe_laboral = FormularioParticipacionCientifica()

            if request.method == "POST":
                try:
                    edit_soporte = ParticipacionCientifica.objects.get(id=id_pcient)
                    expe_laboral = FormularioParticipacionCientifica(
                        request.POST, request.FILES, instance=edit_soporte
                    )
                    id_pcient = 0
                except:
                    expe_laboral = FormularioParticipacionCientifica(
                        request.POST, request.FILES, current_user=request.user.id
                    )

                if expe_laboral.is_valid():
                    expe_laboral.save()
                    queryset_dat = ParticipacionCientifica.objects.filter(
                        nombre_usuario_id=request.user.id
                    )
                    if id_pcient == 0:
                        return redirect("part_cient", id_pcient)

                    else:
                        contexto = {
                            "form": expe_laboral,
                            "querydat": queryset_dat,
                        }
                        return render(
                            request, "participacion_cientifica.html", contexto
                        )
                else:
                    varcond = True
                    contexto = {
                        "form": expe_laboral,
                        "errform": varcond,
                        "id_actual": id_actual,
                    }
                    return render(request, "participacion_cientifica.html", contexto)
            else:
                return render(request, "errores.html", {"form": expe_laboral.errors})
        else:
            return redirect("logear")


class CompetenciasTecnicasComputacionalesHV(View):
    def get(self, request, id_comput=0):
        if request.user.is_authenticated:
            expe_laboral = CompetenciasTecnicasComputacionalesForm(
                current_user=request.user.id
            )
            queryset_dat = CompetenciasTecnicasComputacionale.objects.filter(
                nombre_usuario_id=request.user.id
            )

            url_absoluta = request.build_absolute_uri(settings.MEDIA_URL)
        
            for e in queryset_dat:
                e.documento_url = url_absoluta

            contexto = {
                "form": expe_laboral,
                "querydat": queryset_dat,
            }
            return render(request, "competencias_computacionales.html", contexto)

        else:
            return redirect("logear")

    def post(self, request, id_comput=0):
        if request.user.is_authenticated:
            id_actual = id_comput
            varcond = False
            expe_laboral = CompetenciasTecnicasComputacionalesForm()

            if request.method == "POST":
                try:
                    edit_soporte = CompetenciasTecnicasComputacionale.objects.get(id=id_comput)
                    expe_laboral = CompetenciasTecnicasComputacionalesForm(
                        request.POST, request.FILES, instance=edit_soporte
                    )
                    id_comput = 0
                except:
                    expe_laboral = CompetenciasTecnicasComputacionalesForm(
                        request.POST, request.FILES, current_user=request.user.id
                    )

                if expe_laboral.is_valid():
                    expe_laboral.save()
                    queryset_dat = CompetenciasTecnicasComputacionale.objects.filter(
                        nombre_usuario_id=request.user.id
                    )
                    if id_comput == 0:
                        return redirect("competencia_tecnica", id_comput)

                    else:
                        contexto = {
                            "form": expe_laboral,
                            "querydat": queryset_dat,
                        }
                        return render(
                            request, "competencias_computacionales.html", contexto
                        )
                else:
                    varcond = True
                    contexto = {
                        "form": expe_laboral,
                        "errform": varcond,
                        "id_actual": id_actual,
                    }
                    return render(request, "competencias_computacionales.html", contexto)
            else:
                return render(request, "errores.html", {"form": expe_laboral.errors})
        else:
            return redirect("logear")

def Codigo_vistas_automaticas_get_hv(request,formulario_forms,
                                     models_model,plantilla_html):
    expe_laboral = formulario_forms(
        current_user=request.user.id
    )
    queryset_dat = models_model.objects.filter(
        nombre_usuario_id=request.user.id
    )
    
    url_absoluta = request.build_absolute_uri(settings.MEDIA_URL)

    for e in queryset_dat:
        e.documento_url = url_absoluta

    contexto = {
        "form": expe_laboral,
        "querydat": queryset_dat,
    }

    return (plantilla_html, contexto)
    
def codigo_vistas_automaticas_post_hv(request,formulario_forms,
                                      models_model,plantilla_html, 
                                      refencia_vista,iDD=0):
    id_actual = iDD
    varcond = False
    expe_laboral = formulario_forms()

    if request.method == "POST":
        try:
            edit_soporte = models_model.objects.get(id=iDD)
            expe_laboral = formulario_forms(
                request.POST, request.FILES, instance=edit_soporte
            )
            id_comid_idiomaput = 0
        except:
            expe_laboral = formulario_forms(
                request.POST, request.FILES, current_user=request.user.id
            )

        if expe_laboral.is_valid():
            expe_laboral.save()
            queryset_dat = models_model.objects.filter(
                nombre_usuario_id=request.user.id
            )
            if iDD == 0:
                
                return (refencia_vista,iDD)

            else:
                contexto = {
                    "form": expe_laboral,
                    "querydat": queryset_dat,
                }
 
                return (plantilla_html, contexto)
        else:
            varcond = True
            contexto = {
                "form": expe_laboral,
                "errform": varcond,
                "id_actual": id_actual,
            }
            return (plantilla_html, contexto)
    else:
        plantilla= "errores.html"
        contexto_error={"form": expe_laboral.errors}
        return (plantilla, contexto_error)  
    
class IdiomaExtrangeroHV(View):
    def get(self, request, pasar_id = 0):
        if request.user.is_authenticated:
            plantilla_html, contexto = Codigo_vistas_automaticas_get_hv(request,
                                                                        FormularioIdiomaExtrangero,
                                                                        IdiomaExtrangero,
                                                                        "dominio_idiomas.html")
            return render(request, plantilla_html, contexto)
        else:
            return redirect("logear")
        
    def post(self, request, pasar_id=0):
        if request.user.is_authenticated:
            plantilla, contexto = codigo_vistas_automaticas_post_hv(request,
                                                                    FormularioIdiomaExtrangero,
                                                                    IdiomaExtrangero,"dominio_idiomas.html",
                                                                    "idioma_extangero",pasar_id)
            if contexto==0:
                return redirect(plantilla, contexto)
            return render(request, plantilla,contexto)
            
        else:
            return redirect("logear")
        

