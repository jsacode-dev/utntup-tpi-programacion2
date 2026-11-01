from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table

CONSOLA = Console()

def crear_tabla(titulo: str, columnas: list[str], filas: list[list[object]], color_encabezado: str = "bold cyan") -> Table:
    tabla = Table(title=titulo, header_style=color_encabezado)
    for columna in columnas:
        tabla.add_column(columna)
    for fila in filas:
        tabla.add_row(*(escape(str(celda)) for celda in fila))
    return tabla

def mostrar_tabla(titulo: str, columnas: list[str], filas: list[list[object]]) -> None:
    if not filas:
        mostrar_info("No hay registros para mostrar.")
        return
    CONSOLA.print(crear_tabla(titulo, columnas, filas))

def mostrar_menu(titulo: str, opciones: list[tuple[int, str]]) -> None:
    filas = [[numero, texto] for numero, texto in opciones]
    CONSOLA.print(crear_tabla(titulo, ["Opción", "Descripción"], filas, color_encabezado="bold magenta"))

def mostrar_encabezado(texto: str, subtexto: str = "") -> None:
    CONSOLA.print(Panel(escape(texto), subtitle=escape(subtexto), style="bold magenta"))

def mostrar_error(mensaje: str) -> None:
    CONSOLA.print(f"[bold red]Error:[/] {escape(mensaje)}")

def mostrar_exito(mensaje: str) -> None:
    CONSOLA.print(f"[bold green]OK:[/] {escape(mensaje)}")

def mostrar_info(mensaje: str) -> None:
    CONSOLA.print(f"[bold yellow]Aviso:[/] {escape(mensaje)}")
