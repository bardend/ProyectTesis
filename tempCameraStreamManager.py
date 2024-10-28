from RtspStream import RtspStream
import time
import cv2


class CameraStreamManager:
    def __init__(self):
        self.cameras = {}

    def add_camera(self, id: str, url: str) -> None:
        cam = RtspStream(id, url)
        if cam.startConnection():
            self.cameras[id] = cam
            print(f"Cámara {id} iniciada exitosamente")
            return True
        return False

    def get_frames(self):
        frames = {}
        for id, cam in self.cameras.items():
            frame = cam.get_frame()
            if frame is not None:
                frames[id] = frame
        return frames

    def stop_all(self):
        for cam in self.cameras.values():
            cam.stop()


if __name__ == "__main__":
    # Configuración de las cámaras
    cameras_config = [
        {"id": "cam1", "url": "rtsp://192.168.1.101:8080/h264_ulaw.sdp"},
        #  {"id": "cam2", "url": "rtsp://acecom:1964@192.168.1.100:8080/h264_ulaw.sdp"}
    ]
    # Inicializar manager
    manager = CameraStreamManager()

    # Iniciar todas las cámaras
    for camera in cameras_config:
        manager.add_camera(camera["id"], camera["url"])

    try:
        frame_count = 0
        while True:
            frames = manager.get_frames()
            for id, frame in frames:
                width = 640  # Ajusta según tu resolución
                height = 480
                try:
                    cv2.imshow(f"Camera {id}", frame)
                except ValueError as e:
                    print(f"Error reshaping frame for camera {id}: {e}")
    except KeyboardInterrupt:
        print("Deteniendo cámaras...")
    finally:
        manager.stop_all()
