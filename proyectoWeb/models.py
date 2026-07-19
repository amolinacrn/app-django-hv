from django.db import models
from django.contrib.auth.models import User

class MisPublicaciones(models.Model):
    nombre_usuario = models.ForeignKey(
        User, blank=False, null=False, on_delete=models.CASCADE
    )

    publicaciones_url=models.URLField(max_length=300, blank=True, null=True)

    titulo_publicacion = models.CharField(max_length=200, blank=True,null=True)

    descripcion_publicacion = models.TextField(blank=True,null=True)
    
    imagen_publicacion = models.URLField(max_length=300,blank=True,null=True)

    fecha_publicacion = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    id_video = models.CharField(max_length=50, blank=True,null=True)


