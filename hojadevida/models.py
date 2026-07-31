from django.db import models
from django.contrib.auth.models import User

class FotosPersonale(models.Model):
    nombre_usuario = models.ForeignKey(
        User, blank=False, null=False, on_delete=models.CASCADE
    )
    foto_perfil = models.ImageField(upload_to="files/img/foto", blank=True, null=True)
    imagen_de_portada= models.ImageField(upload_to="files/img/foto",blank=True, null=True)
    imagen_panel_izquierdo= models.ImageField(upload_to="files/img/foto",blank=True, null=True)

class DatosPersonale(models.Model):
    nombre_usuario = models.ForeignKey(
        User, blank=False, null=False, on_delete=models.CASCADE
    )
    documento_identificacion = models.CharField(max_length=50, blank=False, null=False)
    numero_identificacion = models.CharField(max_length=20, blank=False, null=False)
    fecha_expedicion_documento = models.DateField(blank=True, null=True)
    ciudad_expedicion_documento = models.CharField(
        max_length=20, blank=False, null=False
    )
    primer_nombre = models.CharField(max_length=20, blank=False, null=False)
    segundo_nombre = models.CharField(max_length=20, blank=False, null=False)
    primer_apellido = models.CharField(max_length=20, blank=False, null=False)
    segundo_apellido = models.CharField(max_length=20, blank=False, null=False)
    genero_sexual = models.CharField(max_length=15, blank=False, null=False)
    grupo_sanguineo = models.CharField(max_length=15, blank=False, null=False)
    estado_civil = models.CharField(max_length=15, blank=False, null=False)
    pais_origen = models.CharField(max_length=100, blank=False, null=False)
    departamento_origen = models.CharField(max_length=100, blank=False, null=False)
    ciudad_nacimiento = models.CharField(max_length=100, blank=False, null=False)
    nacionalidad = models.CharField(max_length=20, blank=False, null=False)
    fecha_nacimiento = models.DateField(blank=False, null=False)
    ciudad_residencia = models.CharField(max_length=20, blank=False, null=False)
    direccion_residencia = models.CharField(max_length=50, blank=True, null=True)
    telefono_celular = models.CharField(max_length=13, blank=False, null=False)
    correo_electronico = models.EmailField(max_length=50, blank=False, null=False)
    libreta_militar = models.CharField(max_length=15, blank=True, null=True)
    distrito_militar = models.CharField(max_length=5, blank=True, null=True)
    cuenta_github = models.URLField(blank=True, null=True)
    fotocopia_documento = models.FileField(
        upload_to="files/docs/documentid", blank=True, null=True
    )
    perfil_profesional = models.TextField(max_length=1500, blank=True, null=True)
    titulo_mas_reciente = models.CharField(max_length=50, blank=False, null=False)
    universidad_titulo_mas_reciete = models.CharField(max_length=50, blank=False, null=False)
    afiliacion = models.CharField(max_length=300, blank=True, null=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

class TitulosAcademico(models.Model):
    nombre_usuario = models.ForeignKey(
        User, blank=False, null=False, on_delete=models.CASCADE
    )
    grado_academico = models.CharField(max_length=80, blank=False, null=False)
    titulo_obtenido = models.CharField(max_length=80, blank=False, null=False)
    institucion_universitaria = models.CharField(max_length=80, blank=False, null=False)
    programa_academico = models.CharField(max_length=80, blank=True, null=True)
    modalidad_academica = models.CharField(max_length=20, blank=True, null=True)
    fecha_inicio = models.DateField(blank=False, null=False)
    graudado_universitario = models.CharField(max_length=3, blank=False, null=False)
    titulo_disertacion = models.CharField(max_length=200, blank=True, null=True)
    fecha_finalizacion = models.DateField(blank=False, null=False)
    numero_targeta_profesional = models.CharField(max_length=20, blank=True, null=True)
    pais_titulo = models.CharField(max_length=20, blank=False, null=False)
    departamento_titulo = models.CharField(max_length=20, blank=False, null=False)
    ciudad_titulo = models.CharField(max_length=50, blank=True, null=True)
    documento_soporte = models.FileField(
        upload_to="files/docs/diplomas", blank=True, null=True
    )
    cargar_icono = models.ImageField(upload_to="files/img/imgHome/titulos",blank=True, null=True)
    website = models.URLField(max_length=100, blank=True, null=True)
    nit_empresa= models.CharField(max_length=10)

    class Meta:
        ordering = ['fecha_inicio']

class ExperienciasLaborale(models.Model):
    nombre_usuario = models.ForeignKey(
        User, blank=False, null=False, on_delete=models.CASCADE
    )
    tipo_empresa = models.CharField(max_length=80, blank=True, null=True)
    nombre_empresa = models.CharField(max_length=80, blank=False, null=False)
    cargo = models.CharField(max_length=80, blank=False, null=False)
    tipo_contrato = models.CharField(max_length=80, blank=True, null=True)
    departamento_contrato = models.CharField(max_length=20, blank=False, null=False)
    ciudad_contrato = models.CharField(max_length=50, blank=True, null=True)
    pais_contrato = models.CharField(max_length=20, blank=False, null=False)
    contacto_empresa = models.CharField(max_length=12, blank=False, null=False)
    correo_electronico_empresa = models.EmailField(
        max_length=50, blank=True, null=True
    )
    dependencia = models.CharField(max_length=80, blank=True, null=True)
    direccion_empresa = models.CharField(max_length=50, blank=True, null=True)
    fecha_inicio = models.DateField(blank=False, null=False)
    fecha_fin = models.DateField(blank=False, null=False)

    documento_soporte = models.FileField(
        upload_to="files/docs/experiencia", blank=True, null=True
    )
    website = models.URLField(max_length=100, blank=True, null=True)
    cargar_icono = models.ImageField(upload_to="files/img/imgHome/experiencia",blank=True, null=True)
    nit_empresa= models.CharField(max_length=10)

    class Meta:
        ordering = ['-fecha_inicio']

class ProduccionAcademica(models.Model):
    nombre_usuario = models.ForeignKey(
        User, blank=False, null=False, on_delete=models.CASCADE
    )

    tipos_de_productos=models.CharField(max_length=200, blank=True, null=True)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    palabras_clave = models.CharField(max_length=200, blank=True, null=True)
    autores_trabajo = models.CharField(max_length=200, blank=True, null=True)
    nombre_trabajo = models.CharField(max_length=300, blank=True, null=True)
    pais_publicacion = models.CharField(max_length=50, blank=True, null=True)
    fecha_publicacion = models.DateField(blank=False, null=True)
    nombre_revista = models.CharField(max_length=100, blank=True, null=True)
    area_concentracion = models.CharField(max_length=150, blank=True, null=True)
    linea_pesquisa = models.CharField(max_length=150, blank=True, null=True)
    doi_link_publicacion = models.URLField(max_length=100, blank=True, null=True)
    cargar_icono = models.ImageField(upload_to="files/img/imgHome/produccion",blank=True, null=True)
    tecnologias_utilizadas =  models.CharField(max_length=500, blank=True, null=True)
    documento_soporte = models.FileField(
        upload_to="files/docs/papers", blank=True, null=True
    )
    mostrar_producto = models.BooleanField(default=None, blank=True, null=True)
    nit_empresa= models.CharField(max_length=10)
    class Meta:
        ordering = ['-fecha_publicacion']

class ParticipacionCientifica(models.Model):
    nombre_usuario = models.ForeignKey(
        User, blank=False, null=False, on_delete=models.CASCADE
    )
    nombre_evento_cientifico = models.CharField(max_length=200, blank=False, null=False)
    tipo_evento = models.CharField(max_length=150, blank=False, null=False)
    institucion_evento = models.CharField(max_length=100, blank=False, null=False)
    ciudad_evento = models.CharField(max_length=50, blank=False, null=False)
    departamento_evento = models.CharField(max_length=50, blank=True, null=True)
    pais_evento = models.CharField(max_length=50, blank=False, null=False)
    fecha_inicio_evento = models.DateField(blank=False, null=False)
    fecha_fin_evento = models.DateField(blank=False, null=False)
    modalidad_evento = models.CharField(max_length=30, blank=False, null=False)
    documento_soporte = models.FileField(
        upload_to="files/docs/eventos", blank=True, null=True
    )

    cargar_icono = models.ImageField(upload_to="files/img/imgHome/evento",blank=True, null=True)


class IdiomaExtrangero(models.Model):
    nombre_usuario = models.ForeignKey(
        User, blank=False, null=False, on_delete=models.CASCADE
    )
    tipo_idioma = models.CharField(max_length=30, blank=False, null=False)
    domimio_conversacional = models.CharField(max_length=3, blank=False, null=False)
    dominio_lectura = models.CharField(max_length=3, blank=False, null=False)
    dominio_escritura = models.CharField(max_length=3, blank=False, null=False)
    nevel_certificado = models.CharField(max_length=3, blank=True, null=True)
    institucion_expedicion_certificado = models.CharField(
        max_length=80, blank=True, null=True
    )
    fecha_obtecion_certificado = models.DateField(blank=True, null=True)
    pais_obtencion_certificado = models.CharField(
        max_length=50, blank=True, null=True
    )
    departamento_obtencion_certificado = models.CharField(
        max_length=50, blank=True, null=True
    )
    ciudad_obtencion_certificado = models.CharField(
        max_length=50, blank=True, null=True
    )
    documento_soporte = models.FileField(
        upload_to="files/docs/idiomas", blank=True, null=True
    )
  

class CompetenciasTecnicasComputacionale(models.Model):
    class Meta:
        ordering = ['id']

    nombre_usuario = models.ForeignKey(
        User, blank=False, null=False, on_delete=models.CASCADE
    )
    herramienta_tecnica=models.CharField(max_length=30, blank=False, null=False)
    dominio_basico =models.CharField(max_length=3, blank=False, null=False)
    dominio_medio =models.CharField(max_length=3, blank=False, null=False)
    dominio_avanzado =models.CharField(max_length=3, blank=False, null=False)
    documento_soporte = models.FileField(
        upload_to="files/docs/certificados", blank=True, null=True
    )


    cargar_icono = models.ImageField(upload_to="files/img/imgHome/competencia",blank=True, null=True)


class CursosImpartidos(models.Model):

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.identificador_disciplina} {self.nombre_disciplina}"       

    nombre_usuario = models.ForeignKey(
        User, blank=False, null=False, on_delete=models.CASCADE
    )
    identificador_disciplina = models.CharField(max_length=10, blank=False, null=False)
    nombre_disciplina = models.CharField(max_length=30, blank=False, null=False)
    

class UnidadesCursosImpartidos(models.Model):

    class Meta:
        ordering = ['numero_unidad']

    nombre_usuario = models.ForeignKey(
        User, on_delete=models.CASCADE
    )

    disciplina_o_curso = models.ForeignKey(
        CursosImpartidos, on_delete=models.CASCADE
    ) 

    tematicas =  models.CharField(max_length=100, blank=True, null=True)
    unidades_de_tematica =  models.CharField(max_length=2000, blank=True, null=True)
    numero_unidad = models.IntegerField(blank=True)


class CitasBibliograficas(models.Model):
    class Meta:
        ordering = ['id']
        
    nombre_usuario = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    
    codigo_curso = models.CharField(max_length=100)
    titulo_documento_guia = models.CharField(max_length=500, blank=True, null=True)
    link_bibliografia =  models.URLField(max_length=200, blank=True, null=True)
    nombre_curso=models.CharField(max_length=100)
    tipo_texto_guia = models.CharField(max_length=100 , blank=True, null=True)
    capitulos_texto = models.CharField(max_length=3 , blank=True)

 
class ImprimirHojaDeVida(models.Model):
    nombre_usuario = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    imprimir_estudio = models.BooleanField(default=False)
    imprimir_experiencia = models.BooleanField(default=False)
    imprimir_idioma = models.BooleanField(default=False)
    imprimir_produccion = models.BooleanField(default=False)
    imprimir_participacion = models.BooleanField(default=False)
    imprimir_tecnicas = models.BooleanField(default=False)
    imprimir_perfil = models.BooleanField(default=False)
    imprimir_documentacion = models.BooleanField(default=False)