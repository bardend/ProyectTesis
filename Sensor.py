import threading
import random
import time
from typing import Any, Dict
from dataclasses import dataclass, field
from Subject import Subject
from periferic import Periferic
from RtspStream import RtspStream

@dataclass
class Sensor1(Subject, Periferic):
    shared_map: dict = field(default_factory=dict)
    data: Dict[str, Any] = field(default_factory=dict)
    start_event: threading.Event = threading.Event()  # Nuevo evento
    process_read: threading.Thread = None

    def set_controler(self, map_controler: dict):
        self.shared_map = map_controler

    def start_capture(self):
        self.start_event.set()
        self.process_read = threading.Thread(target=self.set_data)
        self.process_read.start()

    def set_data(self):
        while self.start_event.is_set():
            self.data = {"edad": 25, "data": random.randint(1, 100)}
            self.notify_observers(self.data)
            time.sleep(0.5)

    def stop_capture(self):
        self.start_event.clear()
        self.power_on = False
        if self.process_read is not None:
            self.process_read.join()  # Esperar a que el proceso termine







from multiprocessing import Manager
shared_map = Manager().dict()

sensor = Sensor1("00001", 9.5, 8.5, True, 0, "rtsp://1.45.")
sensor.set_controler(shared_map)

camera1 = RtspStream("00001", 9.5, 8.5, True, 0, "rtsp://192.168.0.4:8080/h264_ulaw.sdp", shared_map)

sensor.attach(camera1)
sensor.start_capture()
