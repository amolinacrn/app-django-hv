from django.urls import include, path
from intereses.views import *

urlpatterns = [
  path("", intereses , name="intereses" )
]
