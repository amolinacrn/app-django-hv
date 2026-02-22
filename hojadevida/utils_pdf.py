
from django.http import HttpResponse
from django.conf import settings
from weasyprint import HTML, CSS
from django.template.loader import render_to_string
import os


def render_pdf_view(template_path, context_dict={}):

    html = render_to_string(template_path, context_dict)

    respuesta_pdf = HttpResponse(content_type="application/pdf")
    respuesta_pdf["Content-Disposition"] = "inline; report.pdf"

    css_url = os.path.join(settings.BASE_DIR, "static/bs532/css/bootstrap.min.css")
    config_url_pdf = os.path.join(settings.BASE_DIR, "static/bs532/css/cssbasepdf.css")
   
    HTML(string=html,base_url=settings.BASE_DIR).write_pdf(respuesta_pdf, stylesheets=[CSS(css_url), CSS(config_url_pdf)])

    return respuesta_pdf
