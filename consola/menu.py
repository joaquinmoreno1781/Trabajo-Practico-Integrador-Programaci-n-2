from abc import ABC, abstractmethod
from consola.lectura import leer_entero

class Menu(ABC):
    def __init__(self, usuario, servicios: dict) -> None:
        self._usuario = usuario
        self._servicios = servicios

    @abstractmethod
    def mostrar(self) -> bool:
        """True solicita cerrar sesión; False finaliza el programa."""
        raise NotImplementedError

    def _ejecutar(self, accion) -> None:
        try:
            accion()
        except Exception as error:
            from excepciones import FoodStoreError
            if isinstance(error, (FoodStoreError, ValueError)):
                from consola.ui import mensaje
                mensaje(str(error), "error")
            else:
                raise
