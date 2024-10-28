# Clase derivada RtspStream
from periferic import Periferic
import subprocess as sp
import time
import numpy as np
from threading import Thread


class RtspStream(Periferic):
    def __init__(self, id: str, url: str ) -> None:
        # Llamamos al constructor de la clase base
        super().__init__(id, True)
        self.url = url

        self.command = [
            'ffmpeg',
            '-rtsp_transport', 'tcp',
            '-stimeout', '5000000',
            '-i', self.url,
            '-f', 'image2pipe',
            '-pix_fmt', 'bgr24',
            '-vcodec', 'rawvideo',
            '-vsync', '0',
            '-flags', 'low_delay',
            '-fflags', 'nobuffer',
            '-'
        ]

        '''
        self.command = [
            'ffmpeg',
            '-rtsp_transport', 'udp',  # Cambiado a UDP para mayor velocidad
            '-stimeout', '1000000',  # Reducido el timeout para más rapidez
            '-i', self.url,
            '-vf', 'scale=500:400',  # Escala la imagen a 500x400
            '-frames:v', '1',  # Captura solo el frame más reciente
            '-f', 'image2pipe',
            '-pix_fmt', 'bgr24',
            '-vcodec', 'rawvideo',
            '-vsync', '0',
            '-flags', 'low_delay',
            '-fflags', 'nobuffer+discardcorrupt',  # Descarta frames corruptos
            '-tune', 'zerolatency',  # Optimiza para latencia mínima
            '-preset', 'ultrafast',  # Usa la preconfiguración más rápida
            '-'
        ]
        '''
        self.pipe = None
        self.running = False
        self.width = 500
        self.width = 400
        #self.height = 1080
        self.frame = None
    def startConnection(self) -> bool:
        try:
            self.pipe = sp.Popen(self.command, stdout=sp.PIPE, stderr=sp.PIPE, bufsize=10 ** 7)
            time.sleep(2)

            if self.pipe.poll() is not None:
                error = self.pipe.stderr.read().decode()
                print(f"Error de FFmpeg en cámara {self.id}: {error}")
                return False

            self.running = True
            # Iniciar thread de captura
            Thread(target=self._capture_frames, daemon=True).start()
            return True
        except Exception as e:
            print(f"Error al iniciar cámara {self.id}")
            return False


    def _capture_frames(self):
        while self.running:
            try:
                if self.pipe.poll() is not None:
                    print(f"FFmpeg process has ended for camera {self.id}")
                    break

                raw_image = self.pipe.stdout.read(self.width * self.height * 3)
                if len(raw_image) == 0:
                    continue

                frame = np.frombuffer(raw_image, dtype='uint8')
                self.frame = frame.reshape((self.height, self.width, 3))

            except Exception as e:
                print(f"Error en captura de frames cámara {self.id}")
                time.sleep(0.1)

    #@frame.getter
    def get_frame(self):
        return self.frame
    def stop(self):
        self.running = False