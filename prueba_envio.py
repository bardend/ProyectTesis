from pythonProject1.RtspStream import RtspStream
from multiprocessing import Manager
from ManagerPeriferic import ManagerPeriferic

def dispositivo_a_json(periferico):
    return {
        "urlImagen": "https://cdn-icons-png.flaticon.com/512/10682/10682263.png",
        "coordenadas": {
            "lat": periferico.latitud,
            "lng": periferico.longitud
        },
        "conectionString": "tuConexionString",
        "idUniversal": periferico.idUniversal,
        "powerOn": periferico.power_on,
        "statePeriferico": periferico._state_periferic,
        "urlVideoStreaming": periferico._url
    }

tester = ManagerPeriferic()
tester.add_periferic("00001", 9.5, 8.5, True, 0, "rtsp://192.168.18.68:8080/h264_ulaw.sdp")
tester.add_periferic("00002", 9.5, 8.5, True, 0, "rtsp://192.168.18.68:8080/h264_ulaw.sdp")

# Crear un diccionario usando los IDs como claves
periferics_dict = {
    periferico.idUniversal: dispositivo_a_json(periferico)
    for periferico in tester.periferics
}

import json
json_data = json.dumps(periferics_dict, indent=4)

# http -> framework -> fastapi, flask, django
print(json_data)
# producer -> respectivo topico por cada periferico para enviar la informacion a kafka.


# consumidor -> leer los datos de kafka y enviarlos a la base de datos.
# base de datos -> guardar la informacion de los perifericos.
# api -> para consultar la informacion de los perifericos.
# front -> para mostrar la informacion de los perifericos.
# docker -> para empaquetar la aplicacion y desplegarla en la nube.
# kubernetes -> para orquestar los contenedores en la nube.
# cloud -> para desplegar la aplicacion en la nube.
# github -> para versionar el codigo.
# jenkins -> para automatizar el despliegue de la aplicacion.
# sonarqube -> para analizar la calidad del codigo.
# prometheus -> para monitorear la aplicacion.
# grafana -> para visualizar las metricas de la aplicacion.
