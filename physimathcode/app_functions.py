from urllib.parse import urlparse, parse_qs
from yt_dlp import YoutubeDL
import logging

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