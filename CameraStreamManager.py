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
        init_time = time.time()
        frame_count = 0
        while True:
            frames = manager.get_frames()

            for id, frame in frames.items():
                print(f"Id: {id}")
                cv2.imshow(f"Camera {id}", frame)

            # Esperar 1ms por tecla - permite cerrar las ventanas y mantiene el GUI respondiendo
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            '''
            for id, frame in frames :
                print(id)
            '''


            frame_count += 1
            '''
            if frame_count % 30 == 0:
                print(f"Frames procesados: {frame_count}")

            time.sleep(0.033)  # ~30 FPS
            '''
    except KeyboardInterrupt:
        print("Deteniendo cámaras...")
    finally:
       #manager.stop_all()
        print(f"FPS: {frame_count/(time.time()-init_time)}")