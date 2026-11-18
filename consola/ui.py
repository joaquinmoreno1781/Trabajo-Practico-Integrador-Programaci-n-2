"""Interfaz visual uniforme para Food Store usando Rich, Questionary y prompt_toolkit.

El selector con flechas dibuja un único marco celeste de esquinas redondeadas:
título centrado, subtítulo, línea divisoria, sección y opciones. La opción activa
se resalta como un botón de ancho completo. El pie queda fuera del marco.
"""
from typing import Sequence
import getpass
import shutil

import questionary
from questionary import Style as QuestionaryStyle
from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text
from prompt_toolkit.application import Application, get_app
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.layout.containers import HSplit, VSplit
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout.processors import PasswordProcessor
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, Dimension
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.styles import Style as PromptStyle

console = Console()

ANCHO = 64                # ancho total del marco
INTERIOR = ANCHO - 5      # espacio entre los bordes verticales
ANCHO_ENTRADA = 48        # ancho compacto de los formularios
CIAN = "#22d3ee"
GRIS = "#94a3b8"
PIE = "FOOD STORE · PROGRAMACIÓN II"


def _tamano_terminal() -> tuple[int, int]:
    """Devuelve (columnas, filas) reales de la terminal, con valores seguros."""
    tamano = shutil.get_terminal_size(fallback=(80, 24))
    return tamano.columns, tamano.lines


def _terminal_reducida(filas_necesarias: int, columnas_necesarias: int = ANCHO) -> bool:
    """Activa un modo simple si la terminal no tiene espacio para dibujar la interfaz."""
    columnas, filas = _tamano_terminal()
    # +1 fila de margen: prompt_toolkit necesita una línea libre extra para el cursor.
    return filas < filas_necesarias + 1 or columnas < columnas_necesarias


def _entrada_simple(etiqueta: str, password: bool = False) -> str:
    """Alternativa accesible cuando la terminal es demasiado pequeña para el formulario gráfico."""
    print(f"\n{etiqueta}")
    try:
        return getpass.getpass("> ") if password else input("> ")
    except (EOFError, KeyboardInterrupt):
        return ""

ESTILO_PREGUNTAS = QuestionaryStyle([
    ("qmark", f"fg:{CIAN} bold"),
    ("question", f"fg:{CIAN} bold"),
    ("answer", "fg:#ffffff bold"),
    ("pointer", f"fg:{CIAN} bold"),
    ("highlighted", f"fg:{CIAN} bold"),
    ("selected", f"fg:{CIAN}"),
    ("instruction", f"fg:{GRIS}"),
    ("text", "fg:#ffffff"),
])

ESTILO_MENU = PromptStyle.from_dict({
    "border": CIAN,
    "brand": f"bold {CIAN}",
    "subtitle": GRIS,
    "divider": GRIS,
    "section": "bold #e2e8f0",
    "user": CIAN,
    "option": "#e2e8f0",
    "selected": "bold #ffffff bg:#155e75",
    "hint": GRIS,
    "footer": GRIS,
    "inputborder": "#475569",
    "entrada": "#ffffff",
    "boton": "bold #ffffff bg:#155e75",
    "boton_foco": "bold #ffffff bg:#0e7490",
})


# ---------------------------------------------------------------- Rich ----
def marco(titulo: str, subtitulo: str = "", contenido: str = "") -> None:
    """Panel estático con el mismo look que el menú."""
    partes = [Align.center(Text(titulo, style=f"bold {CIAN}"))]
    if subtitulo:
        partes.append(Align.center(Text(subtitulo, style=GRIS)))
    partes.append(Rule(style=GRIS))
    if contenido:
        partes.append(Text.from_markup(contenido))
    console.print(Panel(Group(*partes), border_style=CIAN, box=box.ROUNDED,
                        padding=(0, 1), width=ANCHO))
    console.print(Text(PIE, style=GRIS, justify="center"), width=ANCHO)


def titulo(texto: str, subtitulo: str | None = None) -> None:
    marco(texto, subtitulo or "Sistema de gestión de pedidos")


def pantalla_login() -> None:
    marco("FOOD STORE", "Sistema de gestión de pedidos",
          "[bold white]INICIO DE SESIÓN[/bold white]\n"
          "[dim]Ingresá tus credenciales para continuar[/dim]")


def pantalla_menu(nombre: str, usuario: str, opciones: Sequence[tuple[int, str]]) -> None:
    """Menú estático dentro del panel (sin navegación con flechas)."""
    lineas = [f"[bold white]{nombre.upper()}[/bold white]", f"[{CIAN}]{usuario}[/{CIAN}]", ""]
    lineas.extend(f"[{CIAN}]{n}.[/{CIAN}] [white]{e}[/white]" for n, e in opciones)
    marco("FOOD STORE", "Sistema de gestión de pedidos", "\n".join(lineas))


# ------------------------------------------------- selector con flechas ----
def _fila(segmentos: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """Encierra una línea entre bordes verticales, rellenando hasta INTERIOR."""
    usado = sum(len(texto) for _, texto in segmentos)
    relleno = " " * max(0, INTERIOR - usado)
    return [("class:border", "│"), *segmentos, ("", relleno), ("class:border", "│\n")]


def _centrado(texto: str, estilo: str) -> list[tuple[str, str]]:
    izq = max(0, (INTERIOR - len(texto)) // 2)
    return _fila([("", " " * izq), (estilo, texto)])


def _vacia() -> list[tuple[str, str]]:
    return _fila([])


def seleccionar_en_marco(seccion: str, opciones: Sequence[tuple[int, str]], usuario: str = "") -> int:
    """Navegación con ↑ ↓ y ENTER dentro de un único marco celeste."""
    if not opciones:
        return 0
    # El selector dibujado necesita 13 filas fijas (14 con usuario) más una por opción.
    # Si no hay espacio, se usa un selector de texto para evitar "Window too small".
    if _terminal_reducida(len(opciones) + 13 + (1 if usuario else 0), ANCHO):
        print(f"\nFOOD STORE - {seccion.upper()}")
        if usuario:
            print(usuario)
        for numero, etiqueta in opciones:
            print(f"{numero}. {etiqueta}")
        while True:
            try:
                elegido = input("Seleccioná una opción (número): ").strip()
            except (EOFError, KeyboardInterrupt):
                return 0
            if elegido.isdigit() and any(int(elegido) == n for n, _ in opciones):
                return int(elegido)
            print("Opción inválida. Intentá nuevamente.")
    indice = 0
    kb = KeyBindings()

    def contenido():
        f: list[tuple[str, str]] = []
        f.append(("class:border", "╭" + "─" * INTERIOR + "╮\n"))
        f += _vacia()
        f += _centrado("FOOD STORE", "class:brand")
        f += _centrado("Sistema de gestión de pedidos", "class:subtitle")
        f += _vacia()
        f.append(("class:border", "├"))
        f.append(("class:divider", "─" * INTERIOR))
        f.append(("class:border", "┤\n"))
        f += _vacia()
        f += _fila([("", "  "), ("class:section", seccion.upper())])
        if usuario:
            f += _fila([("", "  "), ("class:user", usuario)])
        f += _vacia()
        for pos, (numero, etiqueta) in enumerate(opciones):
            if pos == indice:
                texto = f" ❯ {numero}. {etiqueta}".ljust(INTERIOR - 2)
                f += _fila([("", " "), ("class:selected", texto), ("", " ")])
            else:
                texto = f"   {numero}. {etiqueta}"
                f += _fila([("", " "), ("class:option", texto)])
        f += _vacia()
        f.append(("class:border", "╰" + "─" * INTERIOR + "╯\n"))
        pie_ayuda = "↑ ↓ Navegar   ENTER Seleccionar   Ctrl+C Cancelar"
        f.append(("class:hint", " " * ((ANCHO - len(pie_ayuda)) // 2) + pie_ayuda + "\n"))
        f.append(("class:footer", " " * ((ANCHO - len(PIE)) // 2) + PIE))
        return f

    @kb.add("up")
    def subir(event):
        nonlocal indice
        indice = (indice - 1) % len(opciones)
        event.app.invalidate()

    @kb.add("down")
    def bajar(event):
        nonlocal indice
        indice = (indice + 1) % len(opciones)
        event.app.invalidate()

    @kb.add("enter")
    def aceptar(event):
        event.app.exit(result=opciones[indice][0])

    @kb.add("c-c")
    def cancelar(event):
        event.app.exit(result=0)

    ventana = Window(content=FormattedTextControl(contenido, focusable=True),
                     always_hide_cursor=True, dont_extend_height=True, width=ANCHO)
    app = Application(
        layout=Layout(ventana),
        key_bindings=kb,
        style=ESTILO_MENU,
        full_screen=False,
        mouse_support=False,
        erase_when_done=True,   # cada menú reemplaza al anterior
    )
    return int(app.run() or 0)


def seleccionar(mensaje: str, opciones: Sequence[tuple[int, str]]) -> int:
    """Selector genérico dentro del marco celeste."""
    return seleccionar_en_marco(mensaje, opciones)


# --------------------------------------------------- formulario de login ----
def _caja(cuerpo, ancho_total, estilo, relleno=1):
    """Rodea un contenedor con un borde redondeado de ancho_total columnas."""
    def est():
        return estilo() if callable(estilo) else estilo

    borde = ancho_total - 2
    sup = Window(FormattedTextControl(lambda: [(est(), "╭" + "─" * borde + "╮")]), height=1)
    inf = Window(FormattedTextControl(lambda: [(est(), "╰" + "─" * borde + "╯")]), height=1)
    medio = VSplit([
        Window(width=1, char="│", style=est),
        Window(width=relleno),
        cuerpo,
        Window(width=relleno),
        Window(width=1, char="│", style=est),
    ], width=Dimension.exact(ancho_total))  # sin alto fijo: el cuerpo puede tener varias filas
    # Limitar también el contenedor exterior: sin esta dimensión, prompt_toolkit
    # puede estirar el borde derecho hasta el ancho completo de la terminal.
    return HSplit([sup, medio, inf], width=ancho_total)


def _linea(texto: str, estilo: str, centrado: bool = False, ancho: int = ANCHO - 4) -> Window:
    if centrado:
        texto = texto.center(ancho)
    return Window(FormattedTextControl([(estilo, texto)]), height=1)


def formulario_login() -> tuple[str, str] | None:
    """Formulario de acceso; usa modo simple si la terminal es demasiado pequeña."""
    # El formulario gráfico ocupa exactamente 23 filas y 64 columnas.
    # En terminales pequeñas usamos input/getpass, nunca mostramos el error interno.
    if _terminal_reducida(23, ANCHO):
        print("\n" + "=" * 36)
        print("             FOOD STORE")
        print("       Sistema de gestión de pedidos")
        print("=" * 36)
        print("INICIO DE SESIÓN")
        try:
            mail = input("Mail: ").strip()
            clave = getpass.getpass("Contraseña: ")
            return mail, clave
        except (EOFError, KeyboardInterrupt):
            return None

    interior = ANCHO - 4
    ancho_campo = 32  # campos compactos y centrados
    mail = Buffer(multiline=False)
    clave = Buffer(multiline=False)

    w_mail = Window(
        BufferControl(mail, focusable=True),
        width=Dimension.exact(ancho_campo - 4),
        height=1,
        style="class:entrada",
    )
    w_clave = Window(
        BufferControl(
            clave,
            focusable=True,
            input_processors=[PasswordProcessor(char="•")],
        ),
        width=Dimension.exact(ancho_campo - 4),
        height=1,
        style="class:entrada",
    )

    def foco(ventana):
        return lambda: "class:border" if get_app().layout.has_focus(ventana) else "class:inputborder"

    def boton():
        estilo = "class:boton_foco" if get_app().layout.has_focus(w_boton) else "class:boton"
        ancho_boton = ancho_campo - 2
        return [
            (estilo, " " * ancho_boton + "\n"),
            (estilo, "INGRESAR".center(ancho_boton) + "\n"),
            (estilo, " " * ancho_boton),
        ]

    w_boton = Window(
        FormattedTextControl(boton, focusable=True),
        width=Dimension.exact(ancho_campo - 2),
        height=3,
    )

    cuerpo = HSplit([
        Window(height=1),
        _linea("FOOD STORE", "class:brand", True, interior),
        _linea("Sistema de gestión de pedidos", "class:subtitle", True, interior),
        Window(height=1),
        Window(height=1, char="─", style="class:divider", width=Dimension.exact(interior)),
        Window(height=1),
        _linea("INICIO DE SESIÓN", "class:section"),
        _linea("Mail:", "class:user"),
        VSplit([
            Window(width=Dimension.exact((interior - ancho_campo) // 2)),
            _caja(w_mail, ancho_campo, foco(w_mail)),
        ], width=Dimension.exact(interior)),
        _linea("Contraseña:", "class:user"),
        VSplit([
            Window(width=Dimension.exact((interior - ancho_campo) // 2)),
            _caja(w_clave, ancho_campo, foco(w_clave)),
        ], width=Dimension.exact(interior)),
        VSplit([
            Window(width=Dimension.exact((interior - ancho_campo) // 2)),
            w_boton,
        ], width=Dimension.exact(interior)),
    ], width=Dimension.exact(interior))

    # El formulario completo tiene un ancho fijo de ANCHO columnas.
    contenido = _caja(cuerpo, ANCHO, "class:border")
    ayuda = _linea("Tab/↑ ↓ Cambiar campo   ENTER Continuar   Ctrl+C Cancelar", "class:hint", True, ANCHO)
    pie = _linea(PIE, "class:footer", True, ANCHO)
    raiz = HSplit([
        contenido,
        Window(content=FormattedTextControl([("class:hint", "Tab/↑ ↓ Cambiar campo   ENTER Continuar   Ctrl+C Cancelar")]), width=Dimension.exact(ANCHO), height=1),
        Window(content=FormattedTextControl([("class:footer", PIE)]), width=Dimension.exact(ANCHO), height=1),
    ], width=Dimension.exact(ANCHO))

    kb = KeyBindings()
    kb.add("tab")(focus_next)
    kb.add("down")(focus_next)
    kb.add("s-tab")(focus_previous)
    kb.add("up")(focus_previous)

    @kb.add("enter")
    def _enviar(event):
        if get_app().layout.has_focus(w_mail):
            focus_next(event)
        elif get_app().layout.has_focus(w_clave):
            focus_next(event)
        else:
            event.app.exit(result=(mail.text.strip(), clave.text))

    @kb.add("c-c")
    def _cancelar(event):
        event.app.exit(result=None)

    app = Application(
        layout=Layout(raiz, focused_element=w_mail),
        key_bindings=kb,
        style=ESTILO_MENU,
        full_screen=False,
        mouse_support=False,
        erase_when_done=True,
    )
    return app.run()


# ---------------------------------------------------------- utilidades ----
def panel_texto(titulo_panel: str, contenido: str, tipo: str = "info") -> None:
    """Muestra información o resultados dentro de una ventana visual."""
    estilos = {
        "ok": "bold green",
        "error": "bold red",
        "aviso": "bold yellow",
        "info": "bright_cyan",
    }
    cuerpo = Text.from_markup(str(contenido), style=estilos.get(tipo, "white"))
    console.print(
        Panel(cuerpo, title=f"[bold bright_cyan]{titulo_panel}[/bold bright_cyan]",
              border_style="bright_cyan", box=box.ROUNDED,
              padding=(1, 2), width=ANCHO)
    )


def panel_lista(titulo_panel: str, elementos: Sequence[object], vacio: str = "No hay datos para mostrar.") -> None:
    """Muestra una colección completa dentro de un panel."""
    if not elementos:
        panel_texto(titulo_panel, vacio, "aviso")
        return
    contenido = "\n".join(str(elemento) for elemento in elementos)
    panel_texto(titulo_panel, contenido)


def mensaje(texto: str, tipo: str = "info") -> None:
    """Muestra mensajes del sistema encapsulados en un panel."""
    titulos = {"ok": "Correcto", "error": "Error", "aviso": "Aviso", "info": "Food Store"}
    panel_texto(titulos.get(tipo, "Food Store"), texto, tipo)


def pedir_texto(mensaje: str, password: bool = False) -> str:
    """Solicita un dato en un campo compacto; usa texto simple en terminal pequeña."""
    if _terminal_reducida(4, ANCHO):
        return _entrada_simple(mensaje, password)
    buffer = Buffer(multiline=False)
    procesadores = [PasswordProcessor(char="•")] if password else []
    campo = Window(
        BufferControl(buffer, focusable=True, input_processors=procesadores),
        width=Dimension.exact(ANCHO_ENTRADA - 4),
        height=1,
        style="class:entrada",
    )
    estilo_borde = "class:border"
    ancho_interior = ANCHO_ENTRADA - 2
    superior = Window(
        FormattedTextControl([("class:border", "╭" + "─" * ancho_interior + "╮")]),
        width=Dimension.exact(ANCHO_ENTRADA), height=1,
    )
    medio = VSplit([
        Window(width=1, char="│", style=estilo_borde),
        Window(width=1), campo, Window(width=1),
        Window(width=1, char="│", style=estilo_borde),
    ], width=Dimension.exact(ANCHO_ENTRADA), height=1)
    inferior = Window(
        FormattedTextControl([("class:border", "╰" + "─" * ancho_interior + "╯")]),
        width=Dimension.exact(ANCHO_ENTRADA), height=1,
    )
    etiqueta = Window(
        FormattedTextControl([("class:user", mensaje)]),
        width=Dimension.exact(ANCHO_ENTRADA), height=1,
    )
    raiz = HSplit([etiqueta, superior, medio, inferior], width=Dimension.exact(ANCHO_ENTRADA))
    kb = KeyBindings()

    @kb.add("enter")
    def enviar(event):
        event.app.exit(result=buffer.text)

    @kb.add("c-c")
    def cancelar(event):
        event.app.exit(result=None)

    app = Application(
        layout=Layout(raiz, focused_element=campo),
        key_bindings=kb,
        style=ESTILO_MENU,
        full_screen=False,
        mouse_support=False,
        erase_when_done=True,
    )
    resultado = app.run()
    return resultado or ""


def confirmar(mensaje: str) -> bool:
    """Presenta una confirmación dentro del selector enmarcado."""
    opcion = seleccionar_en_marco(mensaje, [(1, "Sí"), (2, "No")])
    return opcion == 1


def tabla(titulo_tabla: str, encabezados: Sequence[str], filas: Sequence[Sequence[object]]) -> None:
    t = Table(title=titulo_tabla, header_style=f"bold {CIAN}", border_style=CIAN)
    for encabezado in encabezados:
        t.add_column(str(encabezado))
    for fila in filas:
        t.add_row(*(str(valor) for valor in fila))
    console.print(Panel(t, border_style=CIAN, box=box.ROUNDED, width=ANCHO, padding=(1, 1)))