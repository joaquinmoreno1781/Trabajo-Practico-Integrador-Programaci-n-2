from entidades import Categoria
from excepciones import DuplicadoError, OperacionNoPermitidaError
from .base_servicio import BaseServicio

class CategoriaServicio(BaseServicio[Categoria]):
    def crear(self, nombre: str, descripcion: str) -> Categoria:
        if any(c.nombre.casefold() == nombre.strip().casefold() for c in self.listar()): raise DuplicadoError("Ya existe una categoría con ese nombre")
        return self.agregar(Categoria(nombre, descripcion))

    def editar(self, identificador: int, nombre: str | None = None, descripcion: str | None = None) -> Categoria:
        categoria = self.buscar_por_id(identificador)
        nuevo_nombre = nombre.strip() if nombre and nombre.strip() else categoria.nombre
        if any(c.id != identificador and c.nombre.casefold() == nuevo_nombre.casefold() for c in self.listar()): raise DuplicadoError("Ya existe una categoría con ese nombre")
        if nombre and nombre.strip(): categoria.nombre = nombre
        if descripcion and descripcion.strip(): categoria.descripcion = descripcion
        return categoria

    def eliminar(self, identificador: int, productos: list) -> None:
        categoria = self.buscar_por_id(identificador)
        activos = [p for p in productos if not p.eliminado and p.categoria == categoria]
        if activos: raise OperacionNoPermitidaError(f"No se puede eliminar: tiene {len(activos)} producto(s) activo(s)")
        categoria.eliminado = True
