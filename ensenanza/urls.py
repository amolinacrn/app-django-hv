from django.urls import path
from .views import *

urlpatterns = [
    path("", vista_ensenanza, name="docencia"),
]