class Periferic:
    def __init__(self, id:str ,power_on:bool) -> None:
        self.id = id
        self.power_on = power_on
    def startConection(self) -> None:
        """Método compartido por todos los periféricos para iniciar conexión."""


