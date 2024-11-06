from dataclasses import dataclass, field

@dataclass
class Periferic:
    idUniversal: str
    latitud : float
    longitud : float
    _power_on: bool
    _state_periferic: int
    _url: str  # IP de la cámara

    @property
    def power_on(self) -> bool:
        return self._power_on

    @power_on.setter
    def power_on(self, current_on: bool) -> None:
        if not isinstance(current_on, bool):
            raise TypeError("El estado de encendido debe ser un booleano")
        self._power_on = current_on

    @property
    def state_periferic(self) -> int:
        return self._state_periferic

    @state_periferic.setter
    def state_periferic(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("El estado del periférico debe ser un entero")
        self._state_periferic = value

    '''
    def start_conection(self) -> bool:
        """Método compartido por todos los periféricos para iniciar conexión."""
        print(f"Starting connection for {self.id}")
        return True
    '''