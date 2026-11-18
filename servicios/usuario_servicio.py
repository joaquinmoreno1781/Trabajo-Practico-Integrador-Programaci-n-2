from entidades import Usuario
from enums import Rol
from excepciones import DuplicadoError, CredencialesInvalidasError
from .base_servicio import BaseServicio

class UsuarioServicio(BaseServicio[Usuario]):
    def crear(self, nombre: str, apellido: str, mail: str, celular: str, contrasenia: str, rol: Rol) -> Usuario:
        if any(u.mail == mail.strip().lower() for u in self.listar(incluir_eliminados=True)): raise DuplicadoError("El mail ya está registrado")
        return self.agregar(Usuario(nombre, apellido, mail, celular, contrasenia, rol))

    def autenticar(self, mail: str, contrasenia: str) -> Usuario:
        for usuario in self._elementos:
            if usuario.mail == mail.strip().lower() and not usuario.eliminado and usuario.verificar_contrasenia(contrasenia): return usuario
        raise CredencialesInvalidasError("Mail o contraseña incorrectos")

    def editar(self, identificador: int, **datos) -> Usuario:
        usuario = self.buscar_por_id(identificador)
        if "mail" in datos and datos["mail"] and any(u.id != identificador and u.mail == datos["mail"].strip().lower() for u in self.listar(incluir_eliminados=True)): raise DuplicadoError("El mail ya está registrado")
        for campo, valor in datos.items():
            if valor is None or valor == "": continue
            if campo == "contrasenia": usuario.cambiar_contrasenia(valor)
            elif hasattr(type(usuario), campo): setattr(usuario, campo, valor)
        return usuario
