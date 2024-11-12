
import threading
import random
import time
from typing import Any, Dict
from dataclasses import dataclass, field
from Subject import Subject
from periferic import Periferic

@dataclass
class Sensor(Subject, Periferic):
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


        '''
        we define the state of the atack :
        0 dont worry
        1 open camera
        '''

        ini_time = time.time()

        while self.start_event.is_set():
            if time.time() - ini_time > 40:
                break
            if time.time() - ini_time < 10: #[0- 10]
                self.data = {"state": 0}
            elif time.time() - ini_time < 20: #[10 - 20]
                self.data = {"state": 1}
            elif time.time() - ini_time < 30: #[20 - 30]
                self.data = {"state": 0}
            elif time.time() - ini_time < 40: #[30 - 40]
                self.data = {"state": 1}

            self.update_state();
            self.notify_observers(self.data)
            time.sleep(0.5)


    def update_state(self):
        self.shared_map[self.idUniversal] = self.data["state"]

    def stop_capture(self):
        self.start_event.clear()
        if self.process_read is not None:
            print("Vamos a esperar que termine el proceso de lectura de Sensor")
            self.process_read.join()  # Esperar a que el proceso termine

    def stop_periferic(self):
        self.power_on = False
        if self.process_read is not None:
            self.process_read.join()  # Esperar a que el proceso termine
