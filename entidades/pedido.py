from datetime import date
from .base import Base
from .calculable import Calculable
from .detalle_pedido import DetallePedido
from .producto import Producto
from enums import Estado, FormaPago
from excepciones import DatoInvalidoError, StockInsuficienteError, OperacionNoPermitidaError
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .usuario import Usuario

class Pedido(Base, Calculable):
    def __init__(self, usuario: 'Usuario', forma_pago: FormaPago) -> None:
        super().__init__()
        from .usuario import Usuario
        if not isinstance(usuario, Usuario) or usuario.eliminado: raise DatoInvalidoError("El pedido requiere un usuario activo")
        if not isinstance(forma_pago, FormaPago): raise DatoInvalidoError("Forma de pago inválida")
        self.__usuario = usuario
        self.__fecha: date = date.today()
        self.__estado: Estado = Estado.PENDIENTE
        self.__forma_pago = forma_pago
        self.__total: float = 0.0
        self.__detalles: list[DetallePedido] = []

    @property
    def usuario(self) -> 'Usuario': return self.__usuario
    @property
    def fecha(self) -> date: return self.__fecha
    @property
    def estado(self) -> Estado: return self.__estado
    @property
    def forma_pago(self) -> FormaPago: return self.__forma_pago
    @forma_pago.setter
    def forma_pago(self, valor: FormaPago) -> None:
        if not isinstance(valor, FormaPago): raise DatoInvalidoError("Forma de pago inválida")
        self.__forma_pago = valor
    @property
    def total(self) -> float: return self.__total
    @property
    def detalles(self) -> tuple[DetallePedido, ...]: return tuple(self.__detalles)

    def agregar_detalle(self, cantidad: int, producto: Producto) -> None:
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0: raise DatoInvalidoError("La cantidad debe ser mayor a cero")
        if not isinstance(producto, Producto) or producto.eliminado or not producto.disponible: raise OperacionNoPermitidaError("El producto no está disponible")
        existente = self.buscar_detalle_por_producto(producto)
        cantidad_nueva = cantidad + (existente.cantidad if existente else 0)
        if cantidad_nueva > producto.stock: raise StockInsuficienteError(f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}")
        if existente:
            existente.cantidad = cantidad_nueva
        else:
            self.__detalles.append(DetallePedido(cantidad, producto))
        self.calcular_total()

    def buscar_detalle_por_producto(self, producto: Producto) -> DetallePedido | None:
        for detalle in self.__detalles:
            if detalle.producto == producto: return detalle
        return None

    def eliminar_detalle_por_producto(self, producto: Producto) -> None:
        detalle = self.buscar_detalle_por_producto(producto)
        if detalle is not None:
            self.__detalles.remove(detalle)
            self.calcular_total()

    def calcular_total(self) -> None:
        self.__total = sum(detalle.subtotal for detalle in self.__detalles)

    def actualizar_estado(self, nuevo_estado: Estado) -> None:
        transiciones = {Estado.PENDIENTE: (Estado.CONFIRMADO, Estado.CANCELADO),
                        Estado.CONFIRMADO: (Estado.TERMINADO, Estado.CANCELADO)}
        if nuevo_estado not in transiciones.get(self.estado, ()):
            raise OperacionNoPermitidaError(f"No se permite pasar de {self.estado.name} a {nuevo_estado.name}")
        self.__estado = nuevo_estado

    def marcar_eliminado(self) -> None:
        self.eliminado = True
        for detalle in self.__detalles: detalle.eliminado = True

    def __str__(self) -> str:
        return f"Pedido #{self.id} | {self.usuario.nombre} {self.usuario.apellido} | {self.estado.name} | ${self.total:.2f} | {self.fecha}"
