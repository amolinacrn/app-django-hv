from django import forms
from .models import *
from .validator import MaxZiseFileValidator
from .validator import MaxZiseImageValidator
from django.contrib.auth.models import User
from .choises import *
from django.core.validators import RegexValidator
from django.utils.safestring import mark_safe

class FotosPersonalesForm(forms.ModelForm):

    foto_perfil = forms.ImageField(
        label=" ",
        required=False,
        validators=[
            MaxZiseImageValidator(max_img_size=1),
        ],
    )


    imagen_de_portada = forms.ImageField(
        label=" ",
        required=False,
        validators=[
            MaxZiseImageValidator(max_img_size=1),
        ],
    )

    imagen_panel_izquierdo = forms.ImageField(
        label=" ",
        required=False,
        validators=[
            MaxZiseImageValidator(max_img_size=1),
        ],
    )


    class Meta:
        model = FotosPersonale
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop("current_user", None)
        super().__init__(*args, **kwargs)
        # self.fields["foto_perfil"].widget.attrs["class"] = "upload-img green"
        # self.fields["imagen_de_portada"].widget.attrs["class"] = "upload-img green"
        self.fields["nombre_usuario"].disabled = True
        self.fields["nombre_usuario"].initial = self.current_user


class DatosPersonalesForm(forms.ModelForm):
    class Meta:
        model = DatosPersonale
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        # Extraer current_user de los argumentos.
        self.current_user = kwargs.pop("current_user", None)
        super().__init__(*args, **kwargs)
        self.fields["cargar_icono"].widget.attrs["class"] = "upload-img green"
        # # Validar si el usuario actual fue proporcionado.
        if not self.current_user:
            self.fields["nombre_usuario"].disabled = True

        else:
            try:
                # Intentar obtener los datos personales del usuario actual.
                db_obj = DatosPersonale.objects.get(nombre_usuario_id=self.current_user)

                # Asignar valores iniciales a los campos del formulario dinámicamente.
                self._set_initial_fields(db_obj)

            except DatosPersonale.DoesNotExist:
                # Si no existe el objeto, deshabilitar el campo 'nombre_usuario'.
                self.fields["nombre_usuario"].disabled = True
                self.fields["nombre_usuario"].initial = self.current_user

            except Exception as e:
                # Manejar cualquier otro error inesperado.
                raise forms.ValidationError(
                    f"Ocurrió un error al inicializar el formulario: {str(e)}"
                )

    def _set_initial_fields(self, db_obj):
        """
        Asigna valores iniciales a los campos del formulario basados en el objeto db_obj.
        """
        for field_name in self.fields:
            if hasattr(db_obj, field_name):
                self.fields[field_name].initial = getattr(db_obj, field_name)

    cargar_icono = forms.ImageField(
        label="",
        required=False,
        validators=[
            MaxZiseImageValidator(max_img_size=0.3),
        ],
    )


    documento_identificacion = forms.CharField(
    max_length=50,
    label=mark_safe("<span style='color:red'>*</span> Tipo Documento:"),
    required=True,
    widget=forms.Select(choices=TIPO_DOCUMENTO),
    )

    numero_identificacion = forms.CharField(
        label=mark_safe("<span style='color:red'>*</span> Número de documento:"),
        required=True,
        widget=forms.NumberInput(),
    )

    fecha_expedicion_documento = forms.DateField(
        label="Fecha de expedicion:",
        required=False,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
    )

    ciudad_expedicion_documento = forms.CharField(
        max_length=20,
        label=mark_safe("<span style='color:red'>*</span> Ciudad de expedición:"),
        required=True,
    )

    primer_nombre = forms.CharField(
        max_length=20,
        label=mark_safe("<span style='color:red'>*</span> Primer nombre:"),
        required=True,
    )

    segundo_nombre = forms.CharField(
        max_length=20,
        label=mark_safe("<span style='color:red'>*</span> Segundo nombre:"),
        required=True,
    )

    primer_apellido = forms.CharField(
        max_length=20,
        label=mark_safe("<span style='color:red'>*</span> Primer apellido:"),
        required=True,
    )

    segundo_apellido = forms.CharField(
        max_length=20,
        label=mark_safe("<span style='color:red'>*</span> Segundo apellido:"),
        required=True,
    )

    genero_sexual = forms.CharField(
        max_length=15,
        label=mark_safe("<span style='color:red'>*</span> Sexo biológico:"),
        required=True,
        widget=forms.Select(choices=TIPO_SEXO),
    )

    grupo_sanguineo = forms.CharField(
        max_length=15,
        label=mark_safe("<span style='color:red'>*</span> Grupo sanguineo:"),
        required=True,
        widget=forms.Select(choices=TIPO_SANGRE),
    )

    estado_civil = forms.CharField(
        max_length=15,
        label=mark_safe("<span style='color:red'>*</span> Estado civil:"),
        required=True,
        widget=forms.Select(choices=ESTADO_CIVIL_TIPO),
    )

    ciudad_nacimiento = forms.CharField(
        max_length=20,
        label=mark_safe("<span style='color:red'>*</span> Ciudad de nacimiento:"),
        required=True,
    )

    fecha_nacimiento = forms.DateField(
        label=mark_safe("<span style='color:red'>*</span> Fecha de nacimiento:"),
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
    )

    pais_origen = forms.CharField(
        max_length=20,
        label=mark_safe("<span style='color:red'>*</span> País:"),
        required=True,
        widget=forms.Select(choices=LISTA_PAISES_MUNDO),
    )

    departamento_origen = forms.CharField(
        max_length=20,
        label=mark_safe("<span style='color:red'>*</span> Departamento:"),
        required=True,
        widget=forms.Select(choices=DEPARTAMENTOS_COLOMBIA),
    )

    nacionalidad = forms.CharField(
        max_length=20,
        label=mark_safe("<span style='color:red'>*</span> Nacionalidad:"),
        required=True,
        widget=forms.Select(choices=NACIONALIDAD_CLASE),
    )

    ciudad_residencia = forms.CharField(
        max_length=20,
        label=mark_safe("<span style='color:red'>*</span> Ciudad de residencia:"),
        required=True,
    )

    direccion_residencia = forms.CharField(
        max_length=50,
        label="Dirección:",
        required=False
    )

    telefono_celular = forms.CharField(
        max_length=13,
        label=mark_safe("<span style='color:red'>*</span> Celular:"),
        required=True,
        widget=forms.NumberInput(),
    )

    correo_electronico = forms.EmailField(
        max_length=50,
        label=mark_safe("<span style='color:red'>*</span> Correo electrónico:"),
        required=True,
    )

    libreta_militar = forms.CharField(
        max_length=15,
        label="Libreta militar:",
        required=False,
        widget=forms.Select(choices=LIBRETA_MILITAR_CLASE),
    )

    distrito_militar = forms.CharField(
        max_length=5,
        label="Distrito militar:",
        required=False,
        widget=forms.NumberInput(),
    )

    cuenta_github = forms.URLField(
        max_length=50,
        label="Cuenta github:",
        required=False
    )

    fotocopia_documento = forms.FileField(
        label="Fotocopia Cédula (pdf):",
        required=False,
        widget=forms.FileInput(),
        validators=[MaxZiseFileValidator(max_file_size=1)]
    )

    perfil_profesional = forms.CharField(
        max_length=1500,
        label="Perfil profesional:",
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 10,
                "cols": 1,
            }
        ),
    )

    titulo_mas_reciente = forms.CharField(
        max_length=50,
        label=mark_safe("<span style='color:red'>*</span> Último título obtenido:"),
        required=True,
    )

    universidad_titulo_mas_reciete = forms.CharField(
        max_length=50,
        label=mark_safe("<span style='color:red'>*</span> Univerisdad último título:"),
        required=True,
    )

    afiliacion = forms.CharField(
        max_length=300,
        label="Afiliación Institucional:",
        required=False,
        widget=forms.Textarea(
                    attrs={
                        "rows": 2,
                        "cols": 1,
                    }
                ),
    )

    descripcion = forms.CharField(
        max_length=200,
        label="Descripción breve:",
        required=False,
        widget=forms.Textarea(
                    attrs={
                        "rows": 2,
                        "cols": 1,
                    }
                ),
    )

class FormularioTitulosAcademicos(forms.ModelForm):

    class Meta:
        model = TitulosAcademico
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop("current_user", None)
        super().__init__(*args, **kwargs)
        self.fields["nombre_usuario"].disabled = True
        self.fields["nombre_usuario"].initial = self.current_user

    website = forms.URLField(
        max_length=100,
        label="Sitio Web:",
        required=False
    )



    nit_empresa= forms.CharField(
        max_length=10,
        required=True,
        label=mark_safe("<span style='color:red'>*</span> Nit empresa:"),
        widget=forms.NumberInput(),
        validators=[
            RegexValidator(
                regex=r'^\d{1,10}$',
                message="Ingrese un número de hasta 10 dígitos"
            )
        ]
    )

    grado_academico = forms.CharField(
        max_length=80,
        label=mark_safe("<span style='color:red'>*</span> Titulación académica:"),
        required=True,
        widget=forms.Select(choices=GRADO_ACADEMICO_PROFESIONAL),
    )
    titulo_obtenido = forms.CharField(
        max_length=100,
        label=mark_safe("<span style='color:red'>*</span> Título obtenido:"),
        required=True,
    )
    institucion_universitaria = forms.CharField(
        max_length=80,
        label=mark_safe("<span style='color:red'>*</span> Institución universitaria:"),
        required=True,
    )
    programa_academico = forms.CharField(
        max_length=100,
        label=mark_safe("Programa académico:"),
        required=False,
    )
    modalidad_academica  = forms.CharField(
        max_length=20,
        label=mark_safe("<span style='color:red'>*</span> Modalidad académica:"),
        required=True,
        widget=forms.Select(choices=MODALIDAD_ACADEMICA),
    )
    fecha_inicio = forms.DateField(
        label=mark_safe("<span style='color:red'>*</span> Fecha de inicio:"),
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
    )
    graudado_universitario = forms.CharField(
        max_length=80,
        label=mark_safe("<span style='color:red'>*</span> Graduado:"),
        required=True,
        widget=forms.Select(choices=ES_GRADUADO_UNIVERSITARIO),
    )
    titulo_disertacion = forms.CharField(
        max_length=200,
        label="Título trabajo de grado:",
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 2,
                "cols": 1,
            }
        ),
    )
    fecha_finalizacion = forms.DateField(
        label=mark_safe("<span style='color:red'>*</span> Fecha de finalización:"),
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
    )
    numero_targeta_profesional = forms.CharField(
        max_length=20,
        label="Número tarjeta profesional:",
        required=False,
    )
    pais_titulo = forms.CharField(
         max_length=20, label=mark_safe("<span style='color:red'>*</span> País:"), required=True,
         widget=forms.Select(choices=LISTA_PAISES_MUNDO),
         
        )

    departamento_titulo = forms.CharField(
        max_length=20, label=mark_safe("<span style='color:red'>*</span> Departamento:"), required=True,
        widget=forms.Select(choices=DEPARTAMENTOS_COLOMBIA),
    )
    ciudad_titulo = forms.CharField(
        max_length=50, label="Ciudad:", required=False
    )

    documento_soporte = forms.FileField(
        #label=mark_safe("Adjuntar diploma en (<b><span style='color:red'>.pdf</span></b>):"),
        required=False,
        widget=forms.FileInput(),
        validators=[
            MaxZiseFileValidator(max_file_size=1),
        ],
    )

    cargar_icono = forms.ImageField(
        label="",
        required=False,
        validators=[
            MaxZiseImageValidator(max_img_size=0.3),
        ],
    )
    
class FormExperienciaLaboral(forms.ModelForm):

    class Meta:
        model = ExperienciasLaborale
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop("current_user", None)
        super().__init__(*args, **kwargs)
        self.fields["nombre_usuario"].disabled = True
        self.fields["nombre_usuario"].initial = self.current_user

    tipo_empresa = forms.CharField(
        max_length=80,
        label="Tipo Empresa:",
        required=False,
        widget=forms.Select(choices=TIPO_DE_EMPRESA_LABORAL),
    )
    nit_empresa= forms.CharField(
        max_length=10,
        required=True,
        label=mark_safe("<span style='color:red'>*</span> Nit empresa:"),
        widget=forms.NumberInput(),
        validators=[
            RegexValidator(
                regex=r'^\d{1,10}$',
                message="Ingrese un número de hasta 10 dígitos"
            )
        ]
    )
    nombre_empresa = forms.CharField(
        max_length=80,
        label=mark_safe("<span style='color:red'>*</span> Nombre empresa:"),
        required=True,
    )

    cargo = forms.CharField(
        max_length=80,
        label=mark_safe("<span style='color:red'>*</span>  Cargo:"),
        required=True
    )

    tipo_contrato = forms.CharField(
        max_length=50,
        label="Tipo contrato:",
        required=False,
        widget=forms.Select(choices=TITPO_CONTRATO_EMPRESA_LABORAL),
    )

    departamento_contrato = forms.CharField(
        max_length=50,
        label=mark_safe("<span style='color:red'>*</span> Departamento:"),
        required=True,
        widget=forms.Select(choices=DEPARTAMENTOS_COLOMBIA),
    )

    ciudad_contrato = forms.CharField(
        max_length=50,
        label="Ciudad:",
        required=False,
    )

    pais_contrato = forms.CharField(
        max_length=50,
        label=mark_safe("<span style='color:red'>*</span> País:"),
        required=True,
        widget=forms.Select(choices=LISTA_PAISES_MUNDO),
    )

    contacto_empresa = forms.CharField(
        max_length=12,
        required=True,
        label=mark_safe("<span style='color:red'>*</span> Telefono empresa:"),
        widget=forms.NumberInput(),
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Ingrese un número de 10 dígitos"
            )
        ]
    )

    correo_electronico_empresa = forms.EmailField(
        max_length=50,
        label="Email empresa:",
        required=False,
    )

    dependencia = forms.CharField(
        max_length=80,
        label="Dependencia:",
        required=False,
    )

    direccion_empresa = forms.CharField(
        max_length=50,
        label="Dirección empresa:",
        required=False,
    )

    fecha_inicio = forms.DateField(
        label=mark_safe("<span style='color:red'>*</span> Fecha inicio:"),
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
    )

    fecha_fin = forms.DateField(
        label=mark_safe("<span style='color:red'>*</span> Fecha finalización:"),
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
    )



    documento_soporte = forms.FileField(
        #label=mark_safe("Soporte experiencia laboral (<b>.jpg</b>):"),
        required=False,
        widget=forms.FileInput(),
        validators=[
            MaxZiseFileValidator(max_file_size=1),
        ],
    )

    cargar_icono = forms.ImageField(
        label="",
        required=False,
        validators=[
            MaxZiseImageValidator(max_img_size=0.3),
        ],
    )

    website = forms.URLField(
        max_length=100,
        label="Sitio Web:",
        required=False
    )

class FormularioProduccionAcademica(forms.ModelForm):

    class Meta:
        model = ProduccionAcademica
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop("current_user", None)
        super().__init__(*args, **kwargs)
        self.fields["nombre_usuario"].disabled = True
        self.fields["nombre_usuario"].initial = self.current_user

    autores_trabajo = forms.CharField(
        max_length=200,
        label="Nombres de los autores:",
        required=False,
    )

    nit_empresa= forms.CharField(
        max_length=10,
        required=True,
        label=mark_safe("<span style='color:red'>*</span> Nit empresa:"),
        widget=forms.NumberInput(),
        validators=[
            RegexValidator(
                regex=r'^\d{1,10}$',
                message="Ingrese un número de hasta 10 dígitos"
            )
        ]
    )
    
    nombre_trabajo = forms.CharField(
        max_length=300,
        label="Nombre publicación:",
        required=False,
    )

    pais_publicacion = forms.CharField(
        max_length=50,
        label="País:",
        required=False,
        widget=forms.Select(choices=LISTA_PAISES_MUNDO),
    )

    fecha_publicacion = forms.DateField(
        label="Fecha publicaciòn:",
        required=False,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
    )

    nombre_revista = forms.CharField(
        max_length=100,
        label="Nombre revista:",
        required=False,
    )

    area_concentracion = forms.CharField(
        max_length=150,
        label="Area de concentración:",
        required=False,
    )

    linea_pesquisa = forms.CharField(
        max_length=150,
        label="Linea de investigación:",
        required=False,
    )

    doi_link_publicacion = forms.URLField(
        max_length=100,
        label="Link o DOI:",
        required=False,
    )

    documento_soporte = forms.FileField(
        required=False,
        widget=forms.FileInput(),
        validators=[
            MaxZiseFileValidator(max_file_size=1),
        ],
    )

    cargar_icono = forms.ImageField(
        label="",
        required=False,
        validators=[
            MaxZiseImageValidator(max_img_size=0.3),
        ],
    )

    tipos_de_productos = forms.CharField(
        max_length=50,
        label="Tipo de producto:",
        required=False,
        widget=forms.Select(choices=TIPOS_PRODUCTO),
    )

    descripcion = forms.CharField(
        max_length=500,
        label="Descripción:",
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "cols": 1,
            })
    )

    palabras_clave = forms.CharField(
        max_length=200,
        label="Palabras clave:",
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 1,
                "cols": 1,
            })
    )    

    mostrar_producto =forms.TypedChoiceField(
        choices=[(True,"Si"),
                 (False,"No")],
        coerce=lambda x: x == "True",
        widget=forms.Select(),
    )

    tecnologias_utilizadas = forms.CharField(
        max_length=500,
        label="Tecnologías utilizadas:",
        required=False,
    )    

    nit_empresa= forms.CharField(
        max_length=10,
        required=True,
        label=mark_safe("<span style='color:red'>*</span> Código de registro:"),
        widget=forms.NumberInput(),
        validators=[
            RegexValidator(
                regex=r'^\d{1,10}$',
                message="Ingrese un número de hasta 10 dígitos"
            )
        ]
    )

class FormularioParticipacionCientifica(forms.ModelForm):

    class Meta:
        model = ParticipacionCientifica
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop("current_user", None)
        super().__init__(*args, **kwargs)
        self.fields["nombre_usuario"].disabled = True
        self.fields["nombre_usuario"].initial = self.current_user

    nombre_evento_cientifico = forms.CharField(
    max_length=200,
    label=mark_safe("<span style='color:red'>*</span>  Nombre del evento:"),
    required=True,
    )

    tipo_evento = forms.CharField(
        max_length=150,
        label=mark_safe("<span style='color:red'>*</span> Tipo de evento:"),
        required=True,
        widget=forms.Select(choices=TIPO_EVENTO_CIENTIFICO),
    )

    institucion_evento = forms.CharField(
        max_length=100,
        label=mark_safe("<span style='color:red'>*</span>  Institución del evento:"),
        required=True,
    )

    ciudad_evento = forms.CharField(
        max_length=50,
        label=mark_safe("<span style='color:red'>*</span>  Ciudad del evento:"),
        required=True,
    )

    departamento_evento = forms.CharField(
        max_length=50,
        label="Departamento del evento:",
        required=False,
        widget=forms.Select(choices=DEPARTAMENTOS_COLOMBIA),
    )

    pais_evento = forms.CharField(
        max_length=50,
        label=mark_safe("<span style='color:red'>*</span> Pais del evento:"),
        required=True,
        widget=forms.Select(choices=LISTA_PAISES_MUNDO),
    )

    fecha_inicio_evento = forms.DateField(
        label=mark_safe("<span style='color:red'>*</span> Fecha inicio:"),
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
    )

    fecha_fin_evento = forms.DateField(
        label=mark_safe("<span style='color:red'>*</span> Fecha fin:"),
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
    )

    modalidad_evento = forms.CharField(
        max_length=80,
        label=mark_safe("<span style='color:red'>*</span> Rol en el evento:"),
        required=True,
        widget=forms.Select(choices=MODALIDAD_EVENTO_CIENTIFICO),
    )

    documento_soporte = forms.FileField(
        #label=mark_safe("soporte del evento (<b>.pdf</b>):"),
        required=False,
        widget=forms.FileInput(),
        validators=[MaxZiseFileValidator(max_file_size=1)],
    )



    cargar_icono = forms.ImageField(
        label="",
        required=False,
        validators=[
            MaxZiseImageValidator(max_img_size=0.3),
        ],
    )

    nit_empresa= forms.CharField(
        max_length=10,
        required=True,
        label=mark_safe("<span style='color:red'>*</span> Nit universidad:"),
        widget=forms.NumberInput(),
            validators=[
                RegexValidator(
                    regex=r'^\d{1,10}$',
                    message="Ingrese un número de hasta 10 dígitos"
                )
            ]
    )

class FormularioIdiomaExtrangero(forms.ModelForm):

    class Meta:
        model = IdiomaExtrangero
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop("current_user", None)
        super().__init__(*args, **kwargs)
        self.fields["nombre_usuario"].disabled = True
        self.fields["nombre_usuario"].initial = self.current_user

    tipo_idioma = forms.CharField(
    max_length=30,
    label=mark_safe("<span style='color:red'>*</span>  Idioma:"),
    required=True,
    widget=forms.Select(choices=DOMINIO_LENGUAGES),
    )

    domimio_conversacional = forms.CharField(
        max_length=3,
        label=mark_safe("<span style='color:red'>*</span> Dominio conversacional:"),
        required=True,
        widget=forms.Select(choices=NIVEL_SUFICIENCIA_INGLES),
    )

    dominio_lectura = forms.CharField(
        max_length=3,
        label=mark_safe("<span style='color:red'>*</span>  Dominio de la lectura:"),
        required=True,
        widget=forms.Select(choices=NIVEL_SUFICIENCIA_INGLES),
    )

    dominio_escritura = forms.CharField(
        max_length=3,
        label=mark_safe("<span style='color:red'>*</span> Dominio de la escritura:"),
        required=True,
        widget=forms.Select(choices=NIVEL_SUFICIENCIA_INGLES),
    )

    nevel_certificado = forms.CharField(
        max_length=3,
        label=mark_safe("Nivel:"),
        required=False,
        widget=forms.Select(choices=NIVEL_INGLES_CERTIFICADO),
    )

    institucion_expedicion_certificado = forms.CharField(
        max_length=80,
        label=mark_safe("Institución expedición del certificado:"),
        required=False,
    )

    fecha_obtecion_certificado = forms.DateField(
        label=mark_safe("Fecha del certificado:"),
        required=False,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
    )

    pais_obtencion_certificado = forms.CharField(
        max_length=50,
        label=mark_safe("País:"),
        required=False,
        widget=forms.Select(choices=LISTA_PAISES_MUNDO),
    )

    departamento_obtencion_certificado = forms.CharField(
        max_length=50,
        label=mark_safe("Departamento:"),
        required=False,
        widget=forms.Select(choices=DEPARTAMENTOS_COLOMBIA),
    )

    ciudad_obtencion_certificado = forms.CharField(
        max_length=50,
        label=mark_safe("Ciudad:"),
        required=False,
    )

    documento_soporte = forms.FileField(
        label=mark_safe("Soporte certificado de idioma (<b>.pdf</b>):"),
        required=False,
        widget=forms.FileInput(),
        validators=[MaxZiseFileValidator(max_file_size=1)],
    )

    nit_empresa= forms.CharField(
        max_length=10,
        required=True,
        label=mark_safe("<span style='color:red'>*</span> Código de idioma:"),
        widget=forms.Select(choices=CODIGOS_DE_IDIOMAS),
    )


    cargar_icono = forms.ImageField(
        label="",
        required=False,
        validators=[
            MaxZiseImageValidator(max_img_size=0.3),
        ],
    )


class CompetenciasTecnicasComputacionalesForm(forms.ModelForm):

    class Meta:
        model = CompetenciasTecnicasComputacionale
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop("current_user", None)
        super().__init__(*args, **kwargs)
        self.fields["nombre_usuario"].disabled = True
        self.fields["nombre_usuario"].initial = self.current_user


    herramienta_tecnica = forms.CharField(
        max_length=30,
        label=mark_safe("<span style='color:red'>*</span> Competencias técnicas:"),
        required=True,
        widget=forms.Select(choices=COMPETENCIAS_TECNICAS_COMPUTACIONALES),
    )

    dominio_basico = forms.CharField(
        max_length=30,
        label=mark_safe("<span style='color:red'>*</span> Dominio básico:"),
        required=True,
        widget=forms.Select(choices=DOMINIO_BASICO_COMPOTENCIA),
    )

    dominio_medio = forms.CharField(
        max_length=30,
        label=mark_safe("<span style='color:red'>*</span> Dominio medio:"),
        required=True,
        widget=forms.Select(choices=DOMINIO_MEDIO_COMPOTENCIA),
    )

    dominio_avanzado = forms.CharField(
        max_length=30,
        label=mark_safe("<span style='color:red'>*</span> Dominio avanzado:"),
        required=True,
        widget=forms.Select(choices=DOMINIO_AVANZADO_COMPOTENCIA),
    )

    documento_soporte = forms.FileField(
        #label=mark_safe("Agregar certificado (<b>.pdf</b>):"),
        required=False,
        widget=forms.FileInput(),
        validators=[MaxZiseFileValidator(max_file_size=1)],
    )

    cargar_icono = forms.ImageField(
        label="Cargue un ícono de su preferencia",
        required=False,
        validators=[
            MaxZiseImageValidator(max_img_size=0.3),
        ],
    )

class FormCursosImpartidos(forms.ModelForm):
    class Meta:
        model = CursosImpartidos
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop("current_user", None)
        super().__init__(*args, **kwargs)
        self.fields["nombre_usuario"].disabled = True
        self.fields["nombre_usuario"].initial = self.current_user
        
    identificador_disciplina = forms.CharField(
        max_length=10,
        label=mark_safe("<span style='color:red'>*</span> Código disciplina:"),
        required=True,
        widget=forms.NumberInput(),
    )
    nombre_disciplina = forms.CharField(
        max_length=30,
        label=mark_safe("<span style='color:red'>*</span> Nombre de la disciplina:"),
        required=True,
    )

class FormUnidadesCursosImpartidos(forms.ModelForm):
    class Meta:
        model = UnidadesCursosImpartidos
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop("current_user", None)
        super().__init__(*args, **kwargs)
        self.fields["nombre_usuario"].disabled = True
        self.fields["nombre_usuario"].initial = self.current_user
        self.fields["disciplina_o_curso"].empty_label = "Seleccione un curso"

    unidades_de_tematica =  forms.CharField(
        max_length=2000,
        label="Agregue las unidades de ésta temática:",
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 6,
                "cols": 1,
            })
    )

    tematicas =  forms.CharField(
        max_length=100,
        label="Temática:",
        required=False,
    )

    numero_unidad = forms.TypedChoiceField(
        choices=CAPITULOS_LIBRO,
        coerce=int,
        label="Número de unidad:",
        required=False,
    )

class FormCitasBibliograficas(forms.ModelForm):

    codigo_curso = forms.ChoiceField(
        label=mark_safe("<span style='color:red'>*</span> Bibliografía del curso:"),
        required=True,
        choices=[]
    )

    class Meta:
        model = CitasBibliograficas
        exclude=["nombre_curso"]
    
    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop("current_user", None)
        super().__init__(*args, **kwargs)
        self.fields["nombre_usuario"].disabled = True
        self.fields["nombre_usuario"].initial = self.current_user

        self.cursos_queryset= CursosImpartidos.objects.all()   
             
        self.DATOS_DISCIPLINA_CODIGO=[]

        for campos in self.cursos_queryset:
            self.DATOS_DISCIPLINA_CODIGO.append((
                campos.identificador_disciplina,
                campos.nombre_disciplina, 
  
            ))

        self.DATOS_DISCIPLINA_CODIGO = [(None, "Seleccione...")] + self.DATOS_DISCIPLINA_CODIGO
        self.fields["codigo_curso"].choices = self.DATOS_DISCIPLINA_CODIGO 

    titulo_documento_guia = forms.CharField(
        max_length=500,
        label="Cita bibliográfica:",
        required=False,
    )
    
    link_bibliografia =  forms.URLField(
        max_length=200,
        label="url Bibliografía:",
        required=False,
    )

    tipo_texto_guia = forms.CharField(
        max_length=100,
        label="Tipo de recurso:",
        required=False,
        widget=forms.Select(choices=TIPO_TEXTO_GUIA),
    )

    capitulos_texto=forms.CharField(
        max_length=3,
        label="Unidad:",
        required=False,
        widget=forms.Select(choices=CAPITULOS_LIBRO),
    )

class FormImprimirHojaDeVida(forms.ModelForm):
    class Meta:
        model = ImprimirHojaDeVida
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop("current_user", None)
        super().__init__(*args, **kwargs)
        self.fields["nombre_usuario"].disabled = True
        self.fields["nombre_usuario"].initial = self.current_user

    imprimir_estudio = forms.TypedChoiceField(
        choices=IMPRIMIR_DATOS,
        coerce=lambda x: x == "True",
        widget=forms.Select(),
    )
    imprimir_experiencia = forms.TypedChoiceField(
        choices=IMPRIMIR_DATOS,
        coerce=lambda x: x == "True",
        widget=forms.Select(),
    )
    imprimir_idioma =forms.TypedChoiceField(
        choices=IMPRIMIR_DATOS,
        coerce=lambda x: x == "True",
        widget=forms.Select(),
    )
    imprimir_produccion = forms.TypedChoiceField(
        choices=IMPRIMIR_DATOS,
        coerce=lambda x: x == "True",
        widget=forms.Select(),
    )
    imprimir_participacion = forms.TypedChoiceField(
        choices=IMPRIMIR_DATOS,
        coerce=lambda x: x == "True",
        widget=forms.Select(),
    )
    imprimir_tecnicas =forms.TypedChoiceField(
        choices=IMPRIMIR_DATOS,
        coerce=lambda x: x == "True",
        widget=forms.Select(),
    )

    imprimir_perfil =forms.TypedChoiceField(
        choices=IMPRIMIR_DATOS,
        coerce=lambda x: x == "True",
        widget=forms.Select(),
    )

    imprimir_documentacion =forms.TypedChoiceField(
        choices=IMPRIMIR_DATOS,
        coerce=lambda x: x == "True",
        widget=forms.Select(),
    )