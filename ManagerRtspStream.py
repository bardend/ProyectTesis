from multiprocessing import Manager
import time
from dataclasses import dataclass, field
from RtspStream import RtspStream

@dataclass
class ManagerRtspStream:
    shared_map: dict = field(default_factory=lambda: Manager().dict())
    pruebas: list = field(default_factory=list)

    def add_prueba(self, url: str):
        prueba = RtspStream(url, self.shared_map)
        self.pruebas.append(prueba)
        return prueba

    def close_all(self):
        for prueba in self.pruebas:
            prueba.stop_capture()

'''
# Ejemplo de uso con dos cámaras
def main():
    try:
        # Crear el manager
        manager = ManagerRtspStream()

        # Crear dos cámaras
        camera1 = manager.add_prueba("rtsp://192.168.1.101:8080/h264_ulaw.sdp")
        #camera2 = manager.add_prueba("rtsp://192.168.1.102:8080/h264_ulaw.sdp")

        # Iniciar conexiones
        ok1 = camera1.start_conection()
        #ok2 = camera2.start_conection()

        # Iniciar capturas
        if ok1:
            camera1.start_capture()
            print("Cámara 1 iniciada")
        if ok2:
            camera2.start_capture()
            print("Cámara 2 iniciada")
        
        # Monitorear frames de ambas cámaras
        ini = time.time()
        while (time.time() - ini < 10):  # Ejecutar por 10 segundos
            # Procesar frames de cada cámara
            for url in manager.shared_map.keys():
                frame = manager.shared_map[url]
                if frame is not None:
                    print(f"Cámara {url} - Frame shape: {frame.shape}")
                    # Aquí puedes procesar el frame como necesites
                    # Por ejemplo, mostrar la imagen:
                    cv2.imshow(f'Camera: {url}', frame)
                    cv2.waitKey(1)

            time.sleep(0.03)  # ~30 FPS

    except KeyboardInterrupt:
        print("\nDeteniendo el programa...")
    finally:
        # Limpieza
        manager.close_all()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
'''