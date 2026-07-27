from django.urls import include, path
from galeria.views import *

urlpatterns = [
  path("", galeria , name="galeria" )
]
