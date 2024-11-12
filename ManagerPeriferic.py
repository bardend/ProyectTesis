from dataclasses import dataclass, field
from typing import List
from periferic import Periferic

@dataclass
class ManagerPeriferic:

    periferics: List[Periferic] = field(default_factory=list)

    def add_periferic(self, periferic: Periferic):
        self.periferics.append(periferic)

    def show_periferics(self) :
        print(self.periferics)

    def close_all(self):
        for stream in self.periferics:
            stream.stop_capture()

    def update_state_periferic(self, id, new_state):
        for p in self.periferics:
            if p.idUniversal == id :
                p.state_periferic = new_state
