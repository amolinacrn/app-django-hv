from physimathcode.app_functions import funcion_panel_base,User
from django.shortcuts import render
from hojadevida.models import ProduccionAcademica

  
def publicaciones(request):
    try:
        user = User.objects.get(username="amolinacrn")
    except User.DoesNotExist:
        user = None

    contexto=funcion_panel_base(request)
    produccion_academica = ProduccionAcademica.objects.filter(nombre_usuario=user)

    for objeto in produccion_academica:
        try:
            objeto.icono_url = request.build_absolute_uri(objeto.cargar_icono.url)
        except Exception:
            objeto.icono_url = None
   
    contexto["queryset_produccion_academica"] = produccion_academica

    return render(request, "publicaciones.html", contexto)  #### cambio aqui: para vista principal