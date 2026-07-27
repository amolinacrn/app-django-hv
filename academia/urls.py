from django.urls import include, path
from academia.views import *

urlpatterns = [
  path("", academia , name="academia" )
]
