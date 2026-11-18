from typing import TypeVar, Generic
from entidades import Base
from excepciones import EntidadNoEncontradaError

T = TypeVar("T", bound=Base)

class BaseServicio(Generic[T]):
    def __init__(self) -> None:
        self._elementos: list[T] = []

    def listar(self, incluir_eliminados: bool = False) -> list[T]:
        return [e for e in self._elementos if incluir_eliminados or not e.eliminado]

    def buscar_por_id(self, identificador: int) -> T:
        for elemento in self._elementos:
            if elemento.id == identificador and not elemento.eliminado:
                return elemento
        raise EntidadNoEncontradaError(f"No se encontró una entidad activa con ID {identificador}")

    def agregar(self, elemento: T) -> T:
        self._elementos.append(elemento)
        return elemento

    def eliminar_logico(self, identificador: int) -> None:
        self.buscar_por_id(identificador).eliminado = True
