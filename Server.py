import json
import asyncio
from websockets.server import serve
import socket
from ManagerRtspStream import ManagerRtspStream

# Obtiene la dirección IP local
def getIpAddress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ipaddress = s.getsockname()[0]
    s.close()
    return ipaddress


ipaddress = getIpAddress()
port = 8765


# Servidor WebSocket que solo recibe datos e imprime cada mensaje recibido
async def echo(websocket):
    async for message in websocket:
        print("Mensaje recibido:", message)

        # Intentar cargar el mensaje como JSON
        try:
            request = json.loads(message)
            print("Datos estructurados (JSON):")
            for key, val in request.items():
                print(f"    {key}: {val}")
                if(val == 0) :
                    tester = ManagerRtspStream()
                    tester.add_prueba("rtsp://192.168.0.4:8080/h264_ulaw.sdp")
                    tester.add_prueba("rtsp://192.168.0.4:8080/h264_ulaw.sdp")
                    tester.start_all_capture(30)



        except json.JSONDecodeError:
            # Si no es JSON, solo imprimir el mensaje recibido
            print("Mensaje no estructurado")


# Inicia el servidor
async def main():
    print(f"Servidor activado en ws://{ipaddress}:{port}")
    async with serve(echo, "0.0.0.0", port):
        await asyncio.Future()  # Ejecuta indefinidamente

asyncio.run(main())