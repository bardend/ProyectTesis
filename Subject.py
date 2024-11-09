from dataclasses import dataclass, field
from typing import List, Any, Dict

@dataclass
class Subject:
    observers: List[Any] = field(default_factory=list)

    def attach(self, observer: Any) -> None:
        self.observers.append(observer)

    def detach(self, observer: Any) -> None:
        self.observers.remove(observer)

    def notify_observers(self, data: Dict[str, Any]) -> None:
        for observer in self.observers:
            observer.update(data)