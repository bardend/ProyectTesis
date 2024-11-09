from abc import ABC, abstractmethod
from typing import List, Any, Dict

class Observer(ABC):
    @abstractmethod
    def update(self, data: Dict[str, Any]) -> None:
        pass
