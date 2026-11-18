from entidades import Pedido
from enums import Estado
from excepciones import EntidadNoEncontradaError, StockInsuficienteError, DatoInvalidoError, OperacionNoPermitidaError
from .base_servicio import BaseServicio

class PedidoServicio(BaseServicio[Pedido]):
    def crear(self, usuario, forma_pago, items: list[tuple]) -> Pedido:
        """Valida todos los artículos antes de descontar stock: operación atómica en memoria."""
        pedido = Pedido(usuario, forma_pago)
        cantidades: dict[int, tuple] = {}
        for producto, cantidad in items:
            if producto.id in cantidades:
                cantidades[producto.id] = (producto, cantidades[producto.id][1] + cantidad)
            else:
                cantidades[producto.id] = (producto, cantidad)
        for producto, cantidad in cantidades.values():
            if cantidad <= 0: raise DatoInvalidoError("La cantidad debe ser mayor a cero")
            if producto.eliminado or not producto.disponible: raise OperacionNoPermitidaError(f"Producto no disponible: {producto.nombre}")
            if cantidad > producto.stock: raise StockInsuficienteError(f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}")
        for producto, cantidad in cantidades.values(): pedido.agregar_detalle(cantidad, producto)
        for producto, cantidad in cantidades.values(): producto.stock -= cantidad
        return self.agregar(pedido)

    def actualizar_estado(self, identificador: int, nuevo_estado: Estado) -> Pedido:
        pedido = self.buscar_por_id(identificador)
        if nuevo_estado == Estado.CANCELADO:
            pedido.actualizar_estado(nuevo_estado)
            for detalle in pedido.detalles: detalle.producto.stock += detalle.cantidad
        else:
            pedido.actualizar_estado(nuevo_estado)
        return pedido

    def eliminar(self, identificador: int) -> None:
        pedido = self.buscar_por_id(identificador)
        if pedido.estado not in (Estado.TERMINADO, Estado.CANCELADO):
            for detalle in pedido.detalles: detalle.producto.stock += detalle.cantidad
        pedido.marcar_eliminado()

    def listar_de_usuario(self, usuario) -> list[Pedido]:
        return [p for p in self.listar() if p.usuario == usuario]
