from ManagerPeriferic import ManagerPeriferic
from fastapi import FastAPI

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

app = FastAPI()
tester = ManagerPeriferic()

tester.add_periferic("0001", -12.020121, -77.049450, True, 0, "rtsp://acecom:1964@10.12.1.5:8080/h264_ulaw.sdp")
tester.add_periferic("0002", -12.017687, -77.049579, True, 0, "rtsp://acecom:1964@10.12.1.78:8080/h264_ulaw.sdp")

#https://mrkite-backendmock.hf.space/perifericos
@app.get("/perifericos")
def get_periferics():
    return  {
    periferico.idUniversal: dispositivo_a_json(periferico) for periferico in tester.periferics
    }

    #Cerrar y prender camara -> Multiprocesos python 
    #Base de datos(sqlalchemy), fast_api

    #####################################################################################################
    # Base de datos(aut) -> tu <----> aut (fastapi, http, sqalchemy) :) -> genera_un_token(json web token)
    #Return 

    # Input :Usuario, password
    # Output: id 
    # Definir los end-points
    
    '''
    #End-points
    -Datos en el body :)

    #/login :
        -input user, password
        -output token{id, nombre_usuario, rol, refresh_token()}

    #/regiter :
        -input campos-acordados-discord
        -output bool
    '''
    ######################################################################################################
    # Back (eventos) -> web socket <----------> ayer te mostre

# uvicorn prueba_envio:app --reload --host 0.0.0.0
