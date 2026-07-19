from .models import MisPublicaciones
from django import forms

class FormMisPublicaciones(forms.ModelForm):

    class Meta:
        model = MisPublicaciones
        # fields = "__all__"
        exclude=["nombre_usuario",
                 "fecha_publicacion",
                 "titulo_publicacion",
                 "descripcion_publicacion",
                 "imagen_publicacion",
                 "id_video"]

    publicaciones_url = forms.URLField(
        max_length=300,
        label="Agrega un link",
        required=False,
    )

