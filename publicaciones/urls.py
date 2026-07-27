from django.urls import include, path
from publicaciones.views import *

urlpatterns = [
  path("", publicaciones , name="publicaciones" )
]
