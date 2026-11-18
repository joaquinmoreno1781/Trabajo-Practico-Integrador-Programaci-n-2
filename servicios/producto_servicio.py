from entidades import Producto
from excepciones import EntidadNoEncontradaError
from .base_servicio import BaseServicio

class ProductoServicio(BaseServicio[Producto]):
    def crear(self, nombre: str, precio: float, descripcion: str, stock: int, imagen: str, disponible: bool, categoria) -> Producto:
        return self.agregar(Producto(nombre, precio, descripcion, stock, imagen, disponible, categoria))

    def editar(self, identificador: int, **datos) -> Producto:
        producto = self.buscar_por_id(identificador)
        for campo, valor in datos.items():
            if valor is not None and hasattr(type(producto), campo): setattr(producto, campo, valor)
        return producto

    def listar_cliente(self) -> list[Producto]:
        return [p for p in self.listar() if p.disponible and p.stock > 0]
