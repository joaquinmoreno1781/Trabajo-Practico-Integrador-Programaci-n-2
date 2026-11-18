from abc import ABC, abstractmethod
from datetime import datetime

class Base(ABC):
    """Clase abstracta común a todas las entidades del sistema."""
    _contador_id: int = 0

    def __init__(self) -> None:
        Base._contador_id += 1
        self.__id: int = Base._contador_id
        self.__eliminado: bool = False
        self.__creado_en: datetime = datetime.now()

    @property
    def id(self) -> int:
        return self.__id

    @property
    def eliminado(self) -> bool:
        return self.__eliminado

    @eliminado.setter
    def eliminado(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise ValueError("El estado eliminado debe ser booleano")
        self.__eliminado = valor

    @property
    def creado_en(self) -> datetime:
        return self.__creado_en

    def __eq__(self, otro: object) -> bool:
        return isinstance(otro, Base) and self.id == otro.id

    @abstractmethod
    def __str__(self) -> str:
        """Devuelve una representación legible de la entidad."""
        raise NotImplementedError
