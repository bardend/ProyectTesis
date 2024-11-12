import random
PARAMS = [
    'ffmpeg',
    '-rtsp_transport', 'tcp',
    '-stimeout', '10000000',
    '-f', 'rawvideo',  # Cambiado a rawvideo para mejor compatibilidad
    '-pix_fmt', 'rgb24',  # Especificar formato de pixel
    '-vsync', '0',  # Desactivar sincronización
    '-b:v', '1000k',
    '-'
]

def periferic_to_inicialization(periferico):
    return {
        #"urlImagen": "https://cdn-icons-png.flaticon.com/512/10682/10682263.png",
        #"coordenadas": {
        #    "lat": periferico.latitud,
        #    "lng": periferico.longitud
        #},
        #"conectionString": "tuConexionString",
        "idUniversal": periferico.idUniversal,
        "powerOn": periferico.power_on,
        "statePeriferico": periferico._state_periferic,
        #"urlVideoStreaming": periferico._url
    }


def send_server_to_ia(frames):
    return [random.randint(0, 10) for _ in frames]



