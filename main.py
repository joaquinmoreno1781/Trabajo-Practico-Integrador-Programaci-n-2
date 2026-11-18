"""Punto de entrada de Food Store. Los datos se mantienen en memoria."""

from servicios import CategoriaServicio, ProductoServicio, UsuarioServicio, PedidoServicio
from enums import Rol
from consola import MenuAdministrador, MenuCliente
from excepciones import CredencialesInvalidasError
from consola.ui import formulario_login, mensaje


def main() -> None:
    """Construye los servicios, carga datos iniciales y administra las sesiones."""
    servicios = {
        "categorias": CategoriaServicio(),
        "productos": ProductoServicio(),
        "usuarios": UsuarioServicio(),
        "pedidos": PedidoServicio(),
    }

    usuarios = servicios["usuarios"]

    # Usuarios iniciales para poder probar ambos roles.
    usuarios.crear(
        "Ana", "Pérez", "admin@foodstore.com", "2610000000", "admin123", Rol.ADMIN
    )
    usuarios.crear(
        "Juan", "Gómez", "juan@foodstore.com", "2611111111", "juan123", Rol.USUARIO
    )

    # Datos de ejemplo cargados en memoria al iniciar el programa.
    categorias = servicios["categorias"]
    cat_hamburguesas = categorias.crear("Hamburguesas", "Hamburguesas y combos")
    cat_bebidas = categorias.crear("Bebidas", "Bebidas frías")

    servicios["productos"].crear(
        "Hamburguesa clásica", 8000, "Carne, queso y vegetales", 10, "", True,
        cat_hamburguesas,
    )
    servicios["productos"].crear(
        "Gaseosa", 2000, "Gaseosa 500 ml", 20, "", True, cat_bebidas,
    )

    while True:
        autenticado = None

        for intento in range(1, 4):
            credenciales = formulario_login()
            if credenciales is None:
                mensaje("Inicio de sesión cancelado. Hasta pronto.", "aviso")
                return

            mail, contrasenia = credenciales
            try:
                autenticado = usuarios.autenticar(mail, contrasenia)
                break
            except CredencialesInvalidasError:
                mensaje("Mail o contraseña incorrectos", "error")
                if intento == 3:
                    mensaje("Se agotaron los 3 intentos. Programa finalizado.", "error")
                    return

        if autenticado is None:
            continue

        mensaje(
            f"Bienvenido/a, {autenticado.nombre} {autenticado.apellido} "
            f"[{autenticado.rol.name}]",
            "ok",
        )

        if autenticado.rol == Rol.ADMIN:
            menu = MenuAdministrador(autenticado, servicios)
        else:
            menu = MenuCliente(autenticado, servicios)

        # mostrar() devuelve False cuando el usuario elige salir del programa.
        if not menu.mostrar():
            mensaje("Hasta pronto", "ok")
            return
        # Si devuelve True, se cerró la sesión y se vuelve al login.


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        mensaje("\nPrograma interrumpido. Hasta pronto.", "aviso")
