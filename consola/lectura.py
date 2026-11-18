from enums import Rol, Estado, FormaPago
from consola.ui import pedir_texto, seleccionar_en_marco, mensaje


def leer_entero(mensaje_entrada: str, minimo: int | None = None) -> int:
    while True:
        try:
            valor = int(pedir_texto(mensaje_entrada))
            if minimo is not None and valor < minimo:
                mensaje(f"Ingrese un número mayor o igual a {minimo}.", "aviso")
                continue
            return valor
        except ValueError:
            mensaje("Ingrese un número entero válido.", "error")


def leer_float(mensaje_entrada: str, minimo: float = 0) -> float:
    while True:
        try:
            valor = float(pedir_texto(mensaje_entrada).replace(",", "."))
            if valor < minimo:
                mensaje(f"El valor debe ser mayor o igual a {minimo}.", "aviso")
                continue
            return valor
        except ValueError:
            mensaje("Ingrese un número válido.", "error")


def elegir_enum(tipo, mensaje_entrada: str):
    opciones = [(opcion.value, opcion.name.replace("_", " ").title()) for opcion in tipo]
    valor = seleccionar_en_marco(mensaje_entrada, opciones)
    for opcion in tipo:
        if opcion.value == valor:
            return opcion
    # Si se cancela, se vuelve a solicitar para no devolver un valor inválido.
    return elegir_enum(tipo, mensaje_entrada)


def confirmar(mensaje_entrada: str) -> bool:
    opcion = seleccionar_en_marco(mensaje_entrada, [(1, "Sí"), (2, "No")])
    return opcion == 1
