import numpy as np
from django import forms
from .models import *
from .validator import MaxZiseFileValidator
from .validator import MaxZiseImageValidator
from django.contrib.auth.models import User
from .choises import *
from django.core.validators import RegexValidator


class FotosPersonalesForm(forms.ModelForm):

    foto_perfil = forms.ImageField(
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
        self.fields["foto_perfil"].widget.attrs["class"] = "upload-img green"
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

    documento_identificacion = forms.CharField(
        max_length=50,
        label="<h7 style='color:red'>*</h7> Tipo Documento:",
        required=True,
        widget=forms.Select(choices=TIPO_DOCUMENTO),
    )

    numero_identificacion = forms.CharField(
        label="<h7 style='color:red'>*</h7> Número de documento:",
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
        label="<h7 style='color:red'>*</h7> Ciudad de expedición:",
        required=True,
    )

    primer_nombre = forms.CharField(
        max_length=20,
        label="<h7 style='color:red'>*</h7> Primer nombre:",
        required=True,
    )

    segundo_nombre = forms.CharField(
        max_length=20,
        label="<h7 style='color:red'>*</h7> Segundo nombre:",
        required=True,
    )

    primer_apellido = forms.CharField(
        max_length=20,
        label="<h7 style='color:red'>*</h7> Primer apellido:",
        required=True,
    )

    segundo_apellido = forms.CharField(
        max_length=20,
        label="<h7 style='color:red'>*</h7> Segundo apellido:",
        required=True,
    )

    genero_sexual = forms.CharField(
        max_length=15,
        label="<h7 style='color:red'>*</h7> Sexo biológico:",
        required=True,
        widget=forms.Select(choices=TIPO_SEXO),
    )

    grupo_sanguineo = forms.CharField(
        max_length=15,
        label="<h7 style='color:red'>*</h7> Grupo sanguineo:",
        required=True,
        widget=forms.Select(choices=TIPO_SANGRE),
    )

    estado_civil = forms.CharField(
        max_length=15,
        label="<h7 style='color:red'>*</h7> Estado civil:",
        required=True,
        widget=forms.Select(choices=ESTADO_CIVIL_TIPO),
    )

    ciudad_nacimiento = forms.CharField(
        max_length=20,
        label="<h7 style='color:red'>*</h7> Ciudad de nacimiento:",
        required=True,
    )

    fecha_nacimiento = forms.DateField(
        label="<h7 style='color:red'>*</h7> Fecha de nacimiento:",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
    )

    pais_origen = forms.CharField(
        max_length=20, label="<h7 style='color:red'>*</h7> País:", required=True,
        widget=forms.Select(choices=LISTA_PAISES_MUNDO),
    )

    departamento_origen = forms.CharField(
        max_length=20, 
        label="<h7 style='color:red'>*</h7> Departamento:",
        required=True,
        widget=forms.Select(choices=DEPARTAMENTOS_COLOMBIA),
    )

    nacionalidad = forms.CharField(
        max_length=20,
        label="<h7 style='color:red'>*</h7> Nacionalidad:",
        required=True,
        widget=forms.Select(choices=NACIONALIDAD_CLASE),
    )

    ciudad_residencia = forms.CharField(
        max_length=20,
        label="<h7 style='color:red'>*</h7> Ciudad de residencia:",
        required=True,
    )

    direccion_residencia = forms.CharField(
        max_length=50, label="Dirección:", required=False
    )

    telefono_celular = forms.CharField(
        max_length=13,
        label="<h7 style='color:red'>*</h7> Celular:",
        required=True,
        widget=forms.NumberInput(),
    )

    correo_electronico = forms.EmailField(
        max_length=50,
        label="<h7 style='color:red'>*</h7> Correo electrónico:",
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
        max_length=50, label="Cuenta github:", required=False
    )

    fotocopia_documento = forms.FileField(
        label="Fotocopia Cédula (pdf):",
        required=False,
        widget=forms.FileInput(),#(attrs={'class': 'upload-img green'}),
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
    label="<h7 style='color:red'>*</h7> Último título obtenido:",
    required=True,
    )

    universidad_titulo_mas_reciete = forms.CharField(
    max_length=50,
    label="<h7 style='color:red'>*</h7> Univerisdad último título:",
    required=True,
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

    grado_academico = forms.CharField(
        max_length=80,
        label="<h7 style='color:red'>*</h7> Titulación académica:",
        required=True,
        widget=forms.Select(choices=GRADO_ACADEMICO_PROFESIONAL),
    )
    titulo_obtenido = forms.CharField(
        max_length=100,
        label="<h7 style='color:red'>*</h7> Título obtenido:",
        required=True,
    )
    institucion_universitaria = forms.CharField(
        max_length=80,
        label="<h7 style='color:red'>*</h7> Institución universitaria:",
        required=True,
    )
    programa_academico = forms.CharField(
        max_length=100,
        label="Programa académico:",
        required=False,
    )
    modalidad_academica  = forms.CharField(
        max_length=20,
        label="<h7 style='color:red'>*</h7> Modalidad académica:",
        required=True,
        widget=forms.Select(choices=MODALIDAD_ACADEMICA),
    )
    fecha_inicio = forms.DateField(
        label="<h7 style='color:red'>*</h7> Fecha de inicio:",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
    )
    graudado_universitario = forms.CharField(
        max_length=80,
        label="<h7 style='color:red'>*</h7> Graduado:",
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
        label="<h7 style='color:red'>*</h7> Fecha de finalización:",
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
         max_length=20, label="<h7 style='color:red'>*</h7> País:", required=True,
         widget=forms.Select(choices=LISTA_PAISES_MUNDO),
         
        )

    departamento_titulo = forms.CharField(
        max_length=20, label="<h7 style='color:red'>*</h7> Departamento:", required=True,
        widget=forms.Select(choices=DEPARTAMENTOS_COLOMBIA),
    )
    ciudad_titulo = forms.CharField(
        max_length=50, label="Ciudad:", required=False
    )

    diploma_titulo = forms.FileField(
        label="Soporte titulación  (<b>.pdf</b>):",
        required=False,
        widget=forms.FileInput(),#(attrs={'class': 'upload-img green'}),
        validators=[
            MaxZiseFileValidator(max_file_size=1),
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
    nombre_empresa = forms.CharField(
        max_length=80,
        label="<h7 style='color:red'>*</h7> Nombre empresa:",
        required=True,
    )
    cargo = forms.CharField(
        max_length=80, label="<h7 style='color:red'>*</h7>  Cargo:", required=True
    )

    tipo_contrato = forms.CharField(
        max_length=50,
        label="Tipo contrato:",
        required=False,
        widget=forms.Select(choices=TITPO_CONTRATO_EMPRESA_LABORAL),
    )
    departamento_contrato = forms.CharField(
        max_length=50,
        label="<h7 style='color:red'>*</h7> Departamento:",
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
        label="<h7 style='color:red'>*</h7> País:",
        required=True,
        widget=forms.Select(choices=LISTA_PAISES_MUNDO),
    )

    contacto_empresa = forms.CharField(
        max_length=12,
        required=True,
        label="<h7 style='color:red'>*</h7> Telefono empresa:",
        widget=forms.NumberInput(),
        validators=[
            RegexValidator(
                regex=r'^\d{12}$',
                message="Ingrese un número de 12 dígitos"
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
        label="<h7 style='color:red'>*</h7> Fecha inicio:",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
    )

    fecha_fin = forms.DateField(
        label="<h7 style='color:red'>*</h7> Fecha finalización:",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
    )
    soportes_experincias_laborales = forms.FileField(
        label="Soporte experiencia laboral (<b>.jpg</b>):",
        required=False,
        widget=forms.FileInput(),
        validators=[
            MaxZiseFileValidator(max_file_size=1),
        ],
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
        label="<h7 style='color:red'>*</h7>  Nombres de los autores:",
        required=True,
    )
    nombre_trabajo = forms.CharField(
        max_length=300,
        label="<h7 style='color:red'>*</h7> Nombre publicación:",
        required=True,
    )
    pais_publicacion = forms.CharField(
        max_length=50,
        label="<h7 style='color:red'>*</h7>  País:",
        required=True,
        widget=forms.Select(choices=LISTA_PAISES_MUNDO),
    )

    fecha_publicacion = forms.DateField(
        label="<h7 style='color:red'>*</h7>  Fecha publicaciòn:",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
    )
    nombre_revista = forms.CharField(
        max_length=100,
        label="<h7 style='color:red'>*</h7> Nombre revista:",
        required=True,
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
        label="<h7 style='color:red'>*</h7> Link o DOI:",
        required=True,
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
        label="<h7 style='color:red'>*</h7>  Nombre del evento:",
        required=True,
    )
    tipo_evento = forms.CharField(
        max_length=150,
        label="<h7 style='color:red'>*</h7> Tipo de evento:",
        required=True,
        widget=forms.Select(choices=TIPO_EVENTO_CIENTIFICO),
    )
    institucion_evento = forms.CharField(
        max_length=100,
        label="<h7 style='color:red'>*</h7>  Institución del evento:",
        required=True,
    )

    ciudad_evento = forms.CharField(
        max_length=50,
        label="<h7 style='color:red'>*</h7>  Ciudad del evento:",
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
        label="<h7 style='color:red'>*</h7> Pais del evento:",
        required=True,
        widget=forms.Select(choices=LISTA_PAISES_MUNDO),
    )
    fecha_inicio_evento = forms.DateField(
        label="<h7 style='color:red'>*</h7> Fecha inicio:",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
    )
    fecha_fin_evento = forms.DateField(
        label="<h7 style='color:red'>*</h7> Fecha fin:",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
    )

    modalidad_evento = forms.CharField(
        max_length=80,
        label="<h7 style='color:red'>*</h7> Rol en el evento:",
        required=True,
        widget=forms.Select(choices=MODALIDAD_EVENTO_CIENTIFICO),
    )

    soportes_eventos_cientificos = forms.FileField(
        label="soporte del evento (<b>.pdf</b>):",
        required=False,
        widget=forms.FileInput(),
        validators=[
            MaxZiseFileValidator(max_file_size=1),
        ],
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
        label="<h7 style='color:red'>*</h7>  Idioma:",
        required=True,
        widget=forms.Select(choices=DOMINIO_LENGUAGES),
    )
    domimio_conversacional = forms.CharField(
        max_length=3,
        label="<h7 style='color:red'>*</h7> Dominio conversacional:",
        required=True,
        widget=forms.Select(choices=NIVEL_SUFICIENCIA_INGLES),
    )
    dominio_lectura = forms.CharField(
        max_length=3,
        label="<h7 style='color:red'>*</h7>  Dominio de la lectura:",
        required=True,
        widget=forms.Select(choices=NIVEL_SUFICIENCIA_INGLES),
    )

    dominio_escritura = forms.CharField(
        max_length=3,
        label="<h7 style='color:red'>*</h7> Dominio de la escritura:",
        required=True,
        widget=forms.Select(choices=NIVEL_SUFICIENCIA_INGLES),
    )
    nevel_certificado = forms.CharField(
        max_length=3,
        label="<h7 style='color:red'>*</h7> Nivel:",
        required=True,
        widget=forms.Select(choices=NIVEL_INGLES_CERTIFICADO),
    )
    institucion_expedicion_certificado = forms.CharField(
        max_length=80,
        label="<h7 style='color:red'>*</h7> Institución expedición del certificado:",
        required=True,
    )
    fecha_obtecion_certificado = forms.DateField(
        label="<h7 style='color:red'>*</h7> Fecha del certificado:",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
    )

    pais_obtencion_certificado = forms.CharField(
        max_length=50,
        label="<h7 style='color:red'>*</h7> País:",
        required=True,
        widget=forms.Select(choices=LISTA_PAISES_MUNDO),
    )

    departamento_obtencion_certificado = forms.CharField(
        max_length=50,
        label="<h7 style='color:red'>*</h7> Departamento:",
        required=True,
        widget=forms.Select(choices=DEPARTAMENTOS_COLOMBIA),
    )

    ciudad_obtencion_certificado = forms.CharField(
        max_length=50,
        label="<h7 style='color:red'>*</h7> Ciudad:",
        required=True,
    )

    soporte_certificado_idioma = forms.FileField(
        label="Soporte certificado de idioma (<b>.pdf</b>):",
        required=False,
        widget=forms.FileInput(),
        validators=[
            MaxZiseFileValidator(max_file_size=1),
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


    herramienta_tecnica=forms.CharField(
        max_length=30,
        label="<h7 style='color:red'>*</h7> Competencias técnicas:",
        required=True,
        widget=forms.Select(choices=COMPETENCIAS_TECNICAS_COMPUTACIONALES),
    )
    dominio_basico =forms.CharField(
        max_length=30,
        label="<h7 style='color:red'>*</h7> Dominio básico:",
        required=True,
        widget=forms.Select(choices=DOMINIO_BASICO_COMPOTENCIA),
    )
    dominio_medio =forms.CharField(
        max_length=30,
        label="<h7 style='color:red'>*</h7> Dominio medio:",
        required=True,
        widget=forms.Select(choices=DOMINIO_MEDIO_COMPOTENCIA),
    )
    dominio_avanzado =forms.CharField(
        max_length=30,
        label="<h7 style='color:red'>*</h7> Dominio avanzado:",
        required=True,
        widget=forms.Select(choices=DOMINIO_AVANZADO_COMPOTENCIA),
    )

    soporte_competencia_computacional = forms.FileField(
        label="Agregar certificado (<b>.pdf</b>):",
        required=False,
        widget=forms.FileInput(),
        validators=[
            MaxZiseFileValidator(max_file_size=1),
        ],
    )