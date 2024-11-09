import time
from dataclasses import dataclass, field
from periferic import Periferic
import threading
import random

@dataclass
class Sensor(Periferic):

    shared_map: dict
    _data: float = field(default=0.0)  # Datos del sensor
    start_event: threading.Event = threading.Event()  #Nuevo evento
    process_read: threading.Thread = None

    @property
    def data(self) -> float:
        return self._data

    @data.setter
    def data(self, current_data: float) -> None:
        self._data = current_data

    def start_conection(self) :
        pass

    def start_capture(self):
        self.start_event.set()
        self.process_read = threading.Thread(target=self.set_data)
        self.process_read.daemon = True
        self.process_read.start()

    def set_data(self):
        while  self.start_event.is_set() and self.power_on:
            self.data = random.randint(1, 100)
            time.sleep(0.5)

    def stop_capture(self):
        self.start_event.clear()
        self.power_on = False
        if self.process_read is not None:
            self.process_read.join()  # Esperar a que el proceso termine

from multiprocessing import Manager
shared_map = Manager().dict()

cur = Sensor("00001", 9.5, 8.5, True, 0, "rtsp://1.45.", shared_map)

cur.start_capture()                 
while True:
    print(cur.data)