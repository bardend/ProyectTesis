import requests
import asyncio
def start_rtsp_stream(url_rtsp):
    try:
        # La URL del endpoint debe coincidir con la definida en FastAPI (/start_stream/)
        response =  requests.post(
            "http://127.0.0.1:8000/start_stream/",
            json={"url": url_rtsp}
        )
        response.raise_for_status()
        print("Respuesta del servidor:", response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error en la petición: {e}")
        return None

if __name__ == "__main__":
    # URL del stream RTSP que quieres iniciar
    rtsp_url = "rtsp://192.168.0.4:8080/h264_ulaw.sdp"
    start_rtsp_stream(rtsp_url)
