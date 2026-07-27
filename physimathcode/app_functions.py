from urllib.parse import urlparse, parse_qs
from yt_dlp import YoutubeDL
import logging
from django.contrib.auth.models import User
from hojadevida.models import FotosPersonale
from django.templatetags.static import static


logger = logging.getLogger(__name__)

def es_acceso_hoja_vida(user):
    return user.is_authenticated and user.groups.filter(
        name="acceso-hoja-de-vida"
    ).exists()

def acceso_hoja_de_vida(user):
    return user.groups.filter(name="acceso-hoja-de-vida").exists()


def obtener_id_youtube(url):

    """
    Obtiene el ID del video de YouTube
    """
    parsed = urlparse(url)
    dominio = parsed.netloc.lower()

    if "youtube.com" in dominio:
        params = parse_qs(parsed.query)

        video_id = params.get("v", [None])[0]    

        if video_id:
            return video_id

    elif "youtu.be" in dominio:
        video_id = parsed.path.strip("/")

        if video_id:
            return video_id

    return None

def es_youtube(url):
    """
    Detecta si la URL es de YouTube
    """

    dominio = urlparse(url).netloc.lower()

    return (
        "youtube.com" in dominio or
        "youtu.be" in dominio
    )

def limpiar_url(url):
    obtner_id=obtener_id_youtube(url)
    if obtner_id:
        return f"https://www.youtube.com/watch?v={obtner_id}"
    return url

def obtener_preview_youtube(url):

    opciones = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
    }

    try:
        with YoutubeDL(opciones) as ydl:
            url = limpiar_url(url)
            info = ydl.extract_info(url, download=False)
            
        return {
            "titulo": info.get("title") or "",
            "descripcion": info.get("description") or "",
            "imagen": info.get("thumbnail") or "",
        }

    except Exception as e:
        logger.exception("Error obteniendo datos de YouTube")
        return {
            "titulo": "",
            "descripcion": "",
            "imagen": "",
        }


def funcion_panel_base(rqst):
    try:
        usuario_login = User.objects.get(username=rqst.user)
    except:
        usuario_login=None

    try:
        user = User.objects.get(username="amolinacrn")
    except User.DoesNotExist:
        user = None
    # --- consultas ---

    foto_obj = FotosPersonale.objects.filter(
        nombre_usuario_id=user
    ).first()

    obj_usuario_login = FotosPersonale.objects.filter(
        nombre_usuario_id=usuario_login
    ).first()

    foto_url_perfil = ""
    url_portada = ""
    url_usuario_login=""
    

    if foto_obj:
        foto_perfil = getattr(foto_obj, "foto_perfil", None)
        portada = getattr(foto_obj, "imagen_de_portada", None)
        obj_usuario_login=getattr(obj_usuario_login, "foto_perfil", None)

        if foto_perfil and foto_perfil.name:
            foto_url_perfil = rqst.build_absolute_uri(foto_perfil.url)
         
        if portada and portada.name:
            url_portada = rqst.build_absolute_uri(portada.url)

        if obj_usuario_login and obj_usuario_login.name:
            url_usuario_login = rqst.build_absolute_uri(obj_usuario_login.url)
        



    # --- icono ---
    eye_icon_static = rqst.build_absolute_uri(
        static("bs532/img/")
    )

    contexto = {
        "eye_icon": eye_icon_static,

        "puede_ver_hv": es_acceso_hoja_vida(rqst.user),

        "foto_perfil": foto_url_perfil,

        "foto_usuario_login":url_usuario_login,
    }

    return contexto