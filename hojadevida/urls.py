from django.urls import path
from hojadevida.views import *


urlpatterns = [
    path("", Menu_HV, name="hojadevida"),
    # path("menuhv", Menu_HV, name="menuhv"),
    path("hoja-de-vida-pdf", view_pdf_HV, name="view_pdf_HV"),
    path("get_phot", formDatPersonView.get_imgfoto, name="get_phot"),
    path("datos_personales", formDatPersonView.get_person_dat, name="get_datos"),
    path("person_dat", formDatPersonView.post_person_dat, name="person_dat"),
    path("phot_profil", formDatPersonView.post_person_phot, name="phot_profil"),
    path("delete_phot", formDatPersonView.phot_delete, name="delete_phot"),
    path("fjspdf", formDatPersonView.getjs_file, name="fjspdf"),
    path("delete_file", formDatPersonView.file_delete, name="delete_file"),
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

    path("delete_regist/<int:id_file>", delete_regist, name="delete_regist"),
    path("delete_expr/<int:id_file>", delete_experience, name="delete_expr"),
    path("delete_pracad/<int:id_file>", delete_prod_acad, name="del_prod_acad"),
    # urls.py
    path("delete/<str:model_name>/<int:pk>/", delete_file_record, name="delete_file_record"),
   

    # path("generando_reporte", GenerandoReporteHV.as_view(), name="gen_report"),
    # path("guardar_foto", views.SuscriptorCreateView.as_view(), name="guardar_foto"),
    # path(
    #     "datos_personales",
    #     DatosPersonalesHV.as_view(),
    #     name="datos_personales",
    # ),
]
