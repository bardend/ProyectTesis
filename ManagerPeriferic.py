from multiprocessing import Manager
import time
from dataclasses import dataclass, field
from RtspStream import RtspStream

@dataclass
class ManagerPeriferic:
    shared_map: dict = field(default_factory=lambda: Manager().dict())
    periferics: list = field(default_factory=list)

    def add_periferic(self, idUniversal: str, latitud: float, longitud: float, power_on: bool, state_periferic: int, url: str):
        cur = RtspStream(idUniversal, latitud, longitud, power_on, state_periferic, url, self.shared_map)
        self.periferics.append(cur)

    def start_all_capture(self, duration=10):
        try :
            for stream in self.periferics:
                ok = stream.start_conection()
                if ok:
                    print(f"Conexión exitosa a {stream._url}")
                    stream.start_capture()
                else:
                    print(f"No se pudo conectar a {stream._url}")

            start_time = time.time()
            while (time.time() - start_time) < duration:
                for url in self.shared_map.keys():
                    frame = self.shared_map[url]
                    print(frame)
                time.sleep(0.03)

            print("Prueba de múltiples cámaras completada")


        except Exception as e:
            print(f"Error durante la prueba: {str(e)}")
        finally:
            self.close_all()

    def close_all(self):
        for stream in self.periferics:
            stream.stop_capture()
'''
if __name__ == "__main__":
    tester = ManagerPeriferic()
    tester.add_periferic("00001", 9.5, 8.5, True, 0, "rtsp://192.168.18.68:8080/h264_ulaw.sdp")
    tester.add_periferic("00002", 9.5, 8.5, True, 0, "rtsp://192.168.18.68:8080/h264_ulaw.sdp")
    tester.start_all_capture(30)
'''