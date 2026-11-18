from .base import Base
from excepciones import DatoInvalidoError
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .producto import Producto

class DetallePedido(Base):
    def __init__(self, cantidad: int, producto: 'Producto') -> None:
        super().__init__()
        self.cantidad = cantidad
        self.producto = producto
        self.__precio_unitario: float = producto.precio
        self.__subtotal: float = self.cantidad * self.__precio_unitario

    @property
    def cantidad(self) -> int: return self.__cantidad
    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0: raise DatoInvalidoError("La cantidad debe ser un entero mayor a cero")
        self.__cantidad = valor
        if hasattr(self, '_DetallePedido__precio_unitario'):
            self.__subtotal = self.__cantidad * self.__precio_unitario

    @property
    def producto(self) -> 'Producto': return self.__producto
    @producto.setter
    def producto(self, valor: 'Producto') -> None:
        from .producto import Producto
        if not isinstance(valor, Producto): raise DatoInvalidoError("Producto inválido")
        self.__producto = valor

    @property
    def subtotal(self) -> float: return self.__subtotal
    @property
    def precio_unitario(self) -> float: return self.__precio_unitario

    def __str__(self) -> str:
        return f"{self.producto.nombre} x {self.cantidad} = ${self.subtotal:.2f}"
