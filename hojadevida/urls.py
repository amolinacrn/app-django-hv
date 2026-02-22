from django.urls import path
from .views import *

urlpatterns = [
    path("", Menu_HV, name="hojadevida"),
    path("hoja-de-vida-pdf", view_pdf_HV, name="view_pdf_HV"),
    path("datos_personales", formDatPersonView.get_person_dat, name="get_datos"),
    path("person_dat", formDatPersonView.post_person_dat, name="person_dat"),
    path("phot_profil", formDatPersonView.post_person_phot, name="phot_profil"),
    path("delete_phot", phot_delete, name="delete_phot"),
    path("delete_file", file_delete, name="delete_file"),

    path(
        "formacion-academica/<int:id_diploma>",
        FormacionAcademicaHV.as_view(),
        name="form_acad",
    ),

    path(
        "Experiencia-laboral/<int:id_explab>",
        ExperienciaLaboralHV.as_view(),
        name="exp_laboral",
    ),
    path(
        "produccion-academica/<int:id_pracad>",
        ProduccionAcademicaHV.as_view(),
        name="prod_acad",
    ),
    path(
        "participacion-cientifica/<int:id_pcient>",
        ParticipacionCientificaHV.as_view(),
        name="part_cient",
    ),

    path(
        "competencia-tecnica/<int:id_comput>",
        CompetenciasTecnicasComputacionalesHV.as_view(),
        name="competencia_tecnica",
    ),

    path(
        "idioma-extangero/<int:pasar_id>",
        IdiomaExtrangeroHV.as_view(),
        name="idioma_extangero",
    ),


    path("delete/<str:model_name>/<int:pk>/", delete_file_record, name="delete_file_record"),

]
