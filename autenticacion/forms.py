from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PermisosParaDocente
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate



class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="",
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Nombre de usuario",
                                       "style": "font-size: 15px;"
                                      }),
    )
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={"placeholder": "Contraseña",
                                      "style": "font-size: 15px;",
                                      }),
    )

    # class Meta:
    #     model = AuthenticationForm
    #     fields = ["username", "password"]

class IniciarSesionForm(UserCreationForm):
    username = forms.CharField(
        label="",
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Nombre de usuario",
                                       "style": "font-size: 15px;"
                                      }),
    )
    
    first_name = forms.CharField(
        label="",
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Nombres",
                                       "style": "font-size: 15px;"
                                      }),
    )
    last_name = forms.CharField(
        label="",
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Apellidos",
                                       "style": "font-size: 15px;"
                                      }),
    )
    email = forms.EmailField(
        label="",
        max_length=100,
        widget=forms.EmailInput(attrs={"placeholder": "Correo electrónico",
         "style": "font-size: 15px;"
        }),
    )

    password1 = forms.CharField(
        label="",
        max_length=150,
        widget=forms.PasswordInput(attrs={"placeholder": "Contraseña",
                                       "style": "font-size: 15px;"
                                      }),
    )

    password2 = forms.CharField(
    label="",
    max_length=150,
    widget=forms.PasswordInput(attrs={"placeholder": "Confirme su contraseña",
                                    "style": "font-size: 15px;"
                                    }),
)



    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "email",
        ]

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ["username", "password1", "password2"]:
            self.fields[fieldname].help_text = None  # no muestre textos de advertencias


class PermisosParaDocentesForm(forms.ModelForm):
    class Meta:
        model = PermisosParaDocente
        fields = "__all__"

    cndsn = [None, True, False]

    PERMISOSDOCENTES = []

    for i in cndsn:

        if i == None:
            x = [i, "--------"]
        elif i:
            x = [i, "permitir"]
        else:
            x = [i, "No permitir"]

        PERMISOSDOCENTES.append(x)

    permiso_docente = forms.CharField(
        max_length=10,
        label="Permiso",
        required=False,
        widget=forms.Select(choices=PERMISOSDOCENTES, attrs={"required": "True"}),
    )

    usuario = forms.CharField(
        max_length=50,
        label="",
        required=True,
        initial="o",  # mi_user_name.id_usuario.username,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["usuario"].disabled = True


