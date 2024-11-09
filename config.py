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
