from consola.menu import Menu
from consola.lectura import leer_entero, leer_float, elegir_enum, confirmar
from enums import Rol, Estado, FormaPago
from consola.ui import (
    seleccionar_en_marco, mensaje, pedir_texto, panel_lista,
    panel_texto, tabla,
)


class MenuAdministrador(Menu):
    def mostrar(self) -> bool:
        while True:
            opciones = [
                (1, "Categorías"), (2, "Productos"), (3, "Usuarios"),
                (4, "Pedidos"), (9, "Cerrar sesión"), (0, "Salir"),
            ]
            op = seleccionar_en_marco(
                "MENÚ ADMINISTRADOR", opciones,
                f"{self._usuario.nombre} {self._usuario.apellido}",
            )
            if op == 1:
                self._ejecutar(self._categorias)
            elif op == 2:
                self._ejecutar(self._productos)
            elif op == 3:
                self._ejecutar(self._usuarios)
            elif op == 4:
                self._ejecutar(self._pedidos)
            elif op == 9:
                return True
            elif op == 0:
                return False

    def _categorias(self):
        servicio = self._servicios["categorias"]
        while True:
            op = seleccionar_en_marco("CATEGORÍAS", [
                (1, "Listar"), (2, "Crear"), (3, "Editar"),
                (4, "Eliminar"), (0, "Volver"),
            ])
            if op == 0:
                return
            if op == 1:
                datos = servicio.listar()
                filas = [(x.id, x.nombre, x.descripcion) for x in datos]
                tabla("CATEGORÍAS REGISTRADAS", ["ID", "Nombre", "Descripción"], filas) if filas else mensaje("No hay categorías cargadas", "aviso")
            elif op == 2:
                creado = servicio.crear(pedir_texto("Nombre:"), pedir_texto("Descripción:"))
                panel_texto("CATEGORÍA CREADA", str(creado), "ok")
            elif op == 3:
                identificador = leer_entero("ID: ", 1)
                categoria = servicio.buscar_por_id(identificador)
                nombre = pedir_texto(f"Nombre [{categoria.nombre}]: ")
                descripcion = pedir_texto(f"Descripción [{categoria.descripcion}]: ")
                editada = servicio.editar(identificador, nombre or None, descripcion or None)
                panel_texto("CATEGORÍA ACTUALIZADA", str(editada), "ok")
            elif op == 4:
                identificador = leer_entero("ID: ", 1)
                if confirmar("¿Eliminar categoría?"):
                    servicio.eliminar(identificador, self._servicios["productos"].listar())
                    mensaje("Categoría eliminada", "ok")

    def _productos(self):
        servicio = self._servicios["productos"]
        categorias = self._servicios["categorias"]
        while True:
            op = seleccionar_en_marco("PRODUCTOS", [
                (1, "Listar"), (2, "Crear"), (3, "Editar"),
                (4, "Eliminar"), (0, "Volver"),
            ])
            if op == 0:
                return
            if op == 1:
                datos = servicio.listar()
                filas = [(x.id, x.nombre, f"${x.precio:.2f}", x.stock,
                          x.categoria.nombre if x.categoria else "-") for x in datos]
                tabla("PRODUCTOS REGISTRADOS", ["ID", "Producto", "Precio", "Stock", "Categoría"], filas) if filas else mensaje("No hay productos", "aviso")
            elif op == 2:
                cats = categorias.listar()
                panel_lista("CATEGORÍAS DISPONIBLES", cats, "Primero cree una categoría.")
                if not cats:
                    continue
                categoria = categorias.buscar_por_id(leer_entero("ID categoría: ", 1))
                producto = servicio.crear(
                    pedir_texto("Nombre: "), leer_float("Precio: "),
                    pedir_texto("Descripción: "), leer_entero("Stock: ", 0),
                    pedir_texto("Imagen (texto/ruta): "), confirmar("¿Disponible?"),
                    categoria,
                )
                panel_texto("PRODUCTO CREADO", str(producto), "ok")
            elif op == 3:
                identificador = leer_entero("ID producto: ", 1)
                producto = servicio.buscar_por_id(identificador)
                mensaje("Dejá vacío un campo para conservar su valor actual", "info")
                nombre = pedir_texto(f"Nombre [{producto.nombre}]: ")
                precio = pedir_texto(f"Precio [{producto.precio}]: ")
                stock = pedir_texto(f"Stock [{producto.stock}]: ")
                datos = {}
                if nombre:
                    datos["nombre"] = nombre
                if precio:
                    datos["precio"] = float(precio.replace(",", "."))
                if stock:
                    datos["stock"] = int(stock)
                actualizado = servicio.editar(identificador, **datos)
                panel_texto("PRODUCTO ACTUALIZADO", str(actualizado), "ok")
            elif op == 4:
                identificador = leer_entero("ID: ", 1)
                if confirmar("¿Eliminar producto?"):
                    servicio.eliminar_logico(identificador)
                    mensaje("Producto eliminado", "ok")

    def _usuarios(self):
        servicio = self._servicios["usuarios"]
        while True:
            op = seleccionar_en_marco("USUARIOS", [
                (1, "Listar"), (2, "Crear"), (3, "Editar"),
                (4, "Eliminar"), (0, "Volver"),
            ])
            if op == 0:
                return
            if op == 1:
                datos = servicio.listar()
                filas = [(u.id, u.nombre, u.apellido, u.mail, u.rol.name) for u in datos]
                tabla("USUARIOS REGISTRADOS", ["ID", "Nombre", "Apellido", "Mail", "Rol"], filas) if filas else mensaje("No hay usuarios", "aviso")
            elif op == 2:
                usuario = servicio.crear(
                    pedir_texto("Nombre: "), pedir_texto("Apellido: "),
                    pedir_texto("Mail: "), pedir_texto("Celular: "),
                    pedir_texto("Contraseña:", password=True), elegir_enum(Rol, "Rol: "),
                )
                panel_texto("USUARIO CREADO", str(usuario), "ok")
            elif op == 3:
                identificador = leer_entero("ID: ", 1)
                usuario = servicio.buscar_por_id(identificador)
                nombre = pedir_texto(f"Nombre [{usuario.nombre}]: ")
                apellido = pedir_texto(f"Apellido [{usuario.apellido}]: ")
                mail = pedir_texto(f"Mail [{usuario.mail}]: ")
                celular = pedir_texto(f"Celular [{usuario.celular}]: ")
                actualizado = servicio.editar(
                    identificador, nombre=nombre or None, apellido=apellido or None,
                    mail=mail or None, celular=celular or None,
                )
                panel_texto("USUARIO ACTUALIZADO", str(actualizado), "ok")
            elif op == 4:
                identificador = leer_entero("ID: ", 1)
                usuario = servicio.buscar_por_id(identificador)
                if usuario.id == self._usuario.id:
                    mensaje("No puede eliminarse a sí mismo", "aviso")
                elif confirmar("¿Eliminar usuario?"):
                    servicio.eliminar_logico(identificador)
                    mensaje("Usuario eliminado", "ok")

    def _pedidos(self):
        pedidos = self._servicios["pedidos"]
        usuarios = self._servicios["usuarios"]
        productos = self._servicios["productos"]
        while True:
            op = seleccionar_en_marco("PEDIDOS", [
                (1, "Listar"), (2, "Crear"),
                (3, "Cambiar estado / forma de pago"),
                (4, "Eliminar"), (0, "Volver"),
            ])
            if op == 0:
                return
            if op == 1:
                datos = pedidos.listar()
                filas = [(p.id, f"{p.usuario.nombre} {p.usuario.apellido}",
                          p.estado.name, p.forma_pago.name, f"${p.total:.2f}") for p in datos]
                tabla("PEDIDOS REGISTRADOS", ["ID", "Cliente", "Estado", "Pago", "Total"], filas) if filas else mensaje("No hay pedidos", "aviso")
                for pedido in datos:
                    panel_lista(f"DETALLE DEL PEDIDO #{pedido.id}", pedido.detalles)
            elif op == 2:
                panel_lista("USUARIOS", usuarios.listar())
                usuario = usuarios.buscar_por_id(leer_entero("ID usuario: ", 1))
                pago = elegir_enum(FormaPago, "Forma de pago: ")
                items = []
                while True:
                    panel_lista("PRODUCTOS DISPONIBLES", productos.listar())
                    identificador = leer_entero("ID producto (0 para terminar): ")
                    if identificador == 0:
                        break
                    items.append((productos.buscar_por_id(identificador), leer_entero("Cantidad: ", 1)))
                pedido = pedidos.crear(usuario, pago, items)
                panel_texto("PEDIDO CREADO", f"Pedido #{pedido.id}\nTotal: ${pedido.total:.2f}", "ok")
            elif op == 3:
                identificador = leer_entero("ID pedido: ", 1)
                pedido = pedidos.buscar_por_id(identificador)
                if confirmar("¿Cambiar estado?"):
                    pedidos.actualizar_estado(identificador, elegir_enum(Estado, "Nuevo estado: "))
                if confirmar("¿Cambiar forma de pago?"):
                    pedido.forma_pago = elegir_enum(FormaPago, "Forma de pago: ")
                mensaje("Pedido actualizado", "ok")
            elif op == 4:
                identificador = leer_entero("ID: ", 1)
                if confirmar("¿Eliminar pedido?"):
                    pedidos.eliminar(identificador)
                    mensaje("Pedido eliminado", "ok")
