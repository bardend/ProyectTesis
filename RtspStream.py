import multiprocessing
import time
from dataclasses import dataclass, field
import subprocess as sp
import numpy as np
from typing import Optional, Any, Dict
from periferic import Periferic
from Observer import Observer

@dataclass
class RtspStream(Periferic, Observer):
    
    shared_map: dict # mapa que guarda dispositivos
    _width: int = field(default=500)  # Ancho del frame
    _height: int = field(default=800)  # Alto del frame
    _pipe: sp.Popen = field(default=None, init=False)  # Canal para leer el streaming
    _frame: Optional[Any] = field(default=None)  # Último frame para procesar
    start_event: multiprocessing.Event = field(default_factory=multiprocessing.Event)  # Nuevo evento
    process_read: multiprocessing.Process = field(default=None, init=False)  # Proceso para start_capture

    def __post_init__(self):
        # Inicializa los parámetros de FFmpeg

        self.shared_map[self.idUniversal] = None

        self.params = [
            'ffmpeg',
            '-rtsp_transport', 'tcp',
            '-stimeout', '10000000',
            '-i', self._url,
            '-f', 'rawvideo',  # Cambiado a rawvideo para mejor compatibilidad
            '-pix_fmt', 'rgb24',  # Especificar formato de pixel
            '-vf', f'scale={self._width}:{self._height}',  # Escalar el video
            '-vsync', '0',  # Desactivar sincronización
            '-b:v', '1000k',
            '-'
        ]


    def start_conection(self) -> bool:
        try:
            self._pipe = sp.Popen(self.params, stdout=sp.PIPE, stderr=sp.PIPE, bufsize=10 ** 7, shell=False)
            time.sleep(2)
            if self._pipe.poll() is not None:
                error = self._pipe.stderr.read().decode()
                print(f"Error de FFmpeg en cámara: {error}")
                return False

            self.power_on = True
            return True

        except Exception as e:
            self._power_on = False
            print(f"Error al iniciar cámara: {str(e)}")
            return False

    def update(self, data: Dict[str, Any]) -> None:
        # Logica para abrir iniciar la captura de frames
        print(data)

        if data["state"] == 1 and not self.start_event.is_set():
            print("Vamos a prender")
            #self.start_event.set()
            self.start_capture()

        elif data["state"] == 0 and self.start_event.is_set():
            print("Vamos a apagar")
            #self.start_event.clear()
            self.stop_capture()

        print(self.start_event.is_set())

    def start_capture(self):
        self.start_event.set()
        self.process_read = multiprocessing.Process(target=self.set_frame)
        #self.process_read.daemon = True  # Asegura que el proceso termine cuando el principal termine
        self.process_read.start()

        if self.start_event.wait(timeout=10):  # 10 segundos de timeout
            return True
        else:
            print(f"Timeout esperando inicio de captura para {self._url}")
            self.stop_capture()
            return False

    def set_frame(self):
        frame_size = self._width * self._height * 3  # RGB tiene 3 canales
        print(f"Iniciando captura para cámara: {self._url}")
        while self.power_on and  self.start_event.is_set():
            try:
                raw_image = b''
                while len(raw_image) < frame_size:
                    chunk = self._pipe.stdout.read(frame_size - len(raw_image))
                    if not chunk:
                        print("No hay más datos disponibles")
                        break
                    raw_image += chunk

                if len(raw_image) < frame_size:
                    continue

                try:
                    current_frame = np.frombuffer(raw_image, dtype='uint8')
                    reshaped_frame = current_frame.reshape((self._height, self._width, 3))
                    self.shared_map[self.idUniversal] = reshaped_frame
                except Exception as e:
                    print(f"Error específico en el procesamiento del frame: {str(e)}")
            except Exception as e:
                print(f"Error en la captura de frames: {str(e)}")
                time.sleep(0.5)


    def stop_capture(self):
        self.start_event.clear()
        if self.process_read is not None:
            self.process_read.join()  # Esperar a que el proceso termine
            print("Aquí termina el proceso de la lectura de frames")
        print("Aca nosotros estamos modificando el fucking mapa")
        self.shared_map[self.idUniversal] = None

    def stop_periferic(self):
        self.power_on = False
        if self.process_read is not None:
            self.process_read.join()  # Esperar a que el proceso termine
        self.shared_map[self.idUniversal] = None