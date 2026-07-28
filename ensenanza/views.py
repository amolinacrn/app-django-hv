from django.shortcuts import render
from hojadevida.models import *
from django.templatetags.static import static
from collections import defaultdict

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

    queryset_bibliografia = CitasBibliograficas.objects.all()
    
    codigos=[]
    
    datos_citas=[]

    bibliografia_cursos = defaultdict(lambda: {"codigo": "", "citas": []})

    for citas in queryset_bibliografia:
        datos_citas.append((
            citas.codigo_curso,
            citas.titulo_documento_guia,
            citas.link_bibliografia,
            citas.tipo_texto_guia,
            citas.capitulos_texto
        ))

    for codigo, cita, link, tipo,unidd in datos_citas: 
        bibliografia_cursos[codigo]["codigo"] = codigo
        bibliografia_cursos[codigo]["citas"].append({
            "cita_bib":cita,
            "link_ref":link,  
            "tipo_bib":tipo, 
            "numero_unidd":unidd             
            })

    dict_bibliografia=dict(bibliografia_cursos)   

    datos=[]

    for campos in datos_queryset:
        datos.append((
            campos.disciplina_o_curso.identificador_disciplina,
            campos.disciplina_o_curso.nombre_disciplina,
            campos.tematicas,
            campos.unidades_de_tematica,
            campos.numero_unidad
        ))
        codigos.append(campos.disciplina_o_curso.identificador_disciplina)

    codigos=set(codigos)

    resultado = defaultdict(lambda: {"nombre": "", "contenidos": []})

    for codigo, nombre, unidades, competencias,unidad in datos:

        resultado[codigo]["nombre"] = nombre

        resultado[codigo]["contenidos"].append({
            "unidades_curso": unidades,
            "competencias_unidad": competencias,  
            "numero_unidad":unidad        
        })

    dict_campos=dict(resultado)
 
    table_content = []
  
    for campo in codigos:
        table_content.append({
            "idd": "id"+campo,
            "disciplina":dict_campos[campo]["nombre"],
            "tematicas_curso": dict_campos[campo]["contenidos"],
            "cita_bibliografica": dict_bibliografia.get(campo, {"citas": []})["citas"],
        })

    eye_icon = request.build_absolute_uri(
        static("bs532/img/")
    )

    Contexto =  {
        "puede_ver_hv": es_acceso_hoja_vida(request.user),
        "eye_icon": eye_icon, 
        "datos_cursos_impartidos": table_content,
        "foto_usuario_login":url_usuario_login,
    }

    return render(
        request,
        "ensenanza.html",
        Contexto
    )


