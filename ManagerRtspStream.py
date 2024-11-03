from multiprocessing import Manager
import time
from dataclasses import dataclass, field
from RtspStream import RtspStream

@dataclass
class ManagerRtspStream:
    shared_map: dict = field(default_factory=lambda: Manager().dict())
    streams: list = field(default_factory=list)

    def add_prueba(self, url: str):
        stream = RtspStream(url, self.shared_map)
        self.streams.append(stream)

    def start_all_capture(self, duration=10):
        try :
            for stream in self.streams:
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
        for stream in self.streams:
            stream.stop_capture()
'''
if __name__ == "__main__":
    tester = ManagerRtspStream()
    tester.add_prueba("rtsp://192.168.0.4:8080/h264_ulaw.sdp")
    tester.add_prueba("rtsp://192.168.0.4:8080/h264_ulaw.sdp")
    tester.start_all_capture(30)
'''