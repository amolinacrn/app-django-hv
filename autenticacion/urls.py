from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path("", VRegistro.as_view(), name="autenticacion"),
    path("cerrar_sesion", cerrar_sesion, name="cerrar_sesion"),
    path("logear", logear, name="logear"),
    path("PerUser", PermisosDocentesView.as_view(), name="PerUser"),
    path("acceso-denegado/", views.acceso_denegado, name="acceso_denegado"),
]
