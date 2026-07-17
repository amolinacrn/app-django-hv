from django.shortcuts import render
from hojadevida.models import User,UnidadesCursosImpartidos,CitasBibliograficas
from django.templatetags.static import static
from collections import defaultdict
import numpy as np

def es_acceso_hoja_vida(user):
    return user.is_authenticated and user.groups.filter(
        name="acceso-hoja-de-vida"
    ).exists()


def vista_ensenanza(request):

    try:
        usuario = User.objects.get(username="amolinacrn")
    except User.DoesNotExist:
        usuario = None
    
    datos_queryset = UnidadesCursosImpartidos.objects.select_related(
        "disciplina_o_curso"
        ).filter(
            nombre_usuario_id=usuario.id
            )
    
    queryset_bibliografia = CitasBibliograficas.objects.all()
    
    codigos=[]
    
    datos_citas=[]

    bibliografia_cursos = defaultdict(lambda: {"codigo": "", "citas": []})

    for citas in queryset_bibliografia:
        datos_citas.append((
            citas.codigo_curso,
            citas.titulo_documento_guia,
            citas.link_bibliografia
        ))


    for codigo, cita, link in datos_citas: 
        bibliografia_cursos[codigo]["codigo"] = codigo
        bibliografia_cursos[codigo]["citas"].append({
            "cita_bib":cita,
            "link_ref":link                
            })


    dict_bibliografia=dict(bibliografia_cursos)   



    datos=[]


    for campos in datos_queryset:
        datos.append((
            campos.disciplina_o_curso.identificador_disciplina,
            campos.disciplina_o_curso.nombre_disciplina,
            campos.tematicas,
            campos.unidades_de_tematica
        ))
        codigos.append(campos.disciplina_o_curso.identificador_disciplina)

    codigos=set(codigos)

    resultado = defaultdict(lambda: {"nombre": "", "contenidos": []})

    for codigo, nombre, unidades, competencias in datos:

        resultado[codigo]["nombre"] = nombre

        resultado[codigo]["contenidos"].append({
            "unidades_curso": unidades,
            "competencias_unidad": competencias,          
        })

    dict_campos=dict(resultado)
 
    table_content = []
  
    for campo in codigos:
        table_content.append({
            "idd": "id"+campo,
            "disciplina":dict_campos[campo]["nombre"],
            "tematicas_curso": dict_campos[campo]["contenidos"],
            "cita_bibliografica": dict_bibliografia[campo]["citas"],
        })

    eye_icon = request.build_absolute_uri(
        static("bs532/img/")
    )

    Contexto =  {
        "puede_ver_hv": es_acceso_hoja_vida(request.user),
        "eye_icon": eye_icon, 
        "datos_cursos_impartidos": table_content,
    }

    return render(
        request,
        "ensenanza.html",
        Contexto
    )


