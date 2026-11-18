from consola.menu import Menu
from consola.lectura import leer_entero
from consola.ui import seleccionar_en_marco, mensaje, panel_lista, panel_texto, tabla


class MenuCliente(Menu):
    def mostrar(self) -> bool:
        while True:
            opciones = [
                (1, "Ver categorías"), (2, "Ver productos disponibles"),
                (3, "Mis pedidos"), (4, "Mis datos"),
                (9, "Cerrar sesión"), (0, "Salir"),
            ]
            op = seleccionar_en_marco(
                "MENÚ CLIENTE", opciones,
                f"{self._usuario.nombre} {self._usuario.apellido}",
            )
            if op == 1:
                datos = self._servicios["categorias"].listar()
                panel_lista("CATEGORÍAS", datos, "No hay categorías cargadas.")
            elif op == 2:
                datos = self._servicios["productos"].listar_cliente()
                filas = [(p.id, p.nombre, f"${p.precio:.2f}", p.stock,
                          p.categoria.nombre if p.categoria else "-") for p in datos]
                tabla("PRODUCTOS DISPONIBLES", ["ID", "Producto", "Precio", "Stock", "Categoría"], filas) if filas else mensaje("No hay productos disponibles", "aviso")
            elif op == 3:
                datos = self._servicios["pedidos"].listar_de_usuario(self._usuario)
                filas = [(p.id, p.estado.name, p.forma_pago.name, f"${p.total:.2f}") for p in datos]
                tabla("MIS PEDIDOS", ["ID", "Estado", "Forma de pago", "Total"], filas) if filas else mensaje("No tiene pedidos", "aviso")
                for pedido in datos:
                    panel_lista(f"DETALLE DEL PEDIDO #{pedido.id}", pedido.detalles)
                if datos:
                    identificador = leer_entero("ID de pedido para ver detalles (0 volver): ")
                    for pedido in datos:
                        if pedido.id == identificador:
                            panel_texto(
                                f"PEDIDO #{pedido.id}",
                                "\n".join(str(d) for d in pedido.detalles)
                                + f"\n\nTotal: ${pedido.total:.2f}",
                            )
            elif op == 4:
                contenido = (
                    f"Nombre: {self._usuario.nombre}\n"
                    f"Apellido: {self._usuario.apellido}\n"
                    f"Mail: {self._usuario.mail}\n"
                    f"Celular: {self._usuario.celular}\n"
                    f"Rol: {self._usuario.rol.name}"
                )
                panel_texto("MIS DATOS", contenido)
            elif op == 9:
                return True
            elif op == 0:
                return False
