from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

CONSOLA = Console()

def crear_tabla(titulo: str, columnas: list[str], filas: list[list[object]], color_encabezado: str = "bold cyan") -> Table:
    """Crea una tabla formateada con rich."""
    tabla = Table(title=titulo, title_style="italic", header_style=color_encabezado)
    for columna in columnas:
        tabla.add_column(columna)
    for fila in filas:
        tabla.add_row(*(escape(str(celda)) for celda in fila))
    return tabla

def mostrar_tabla(titulo: str, columnas: list[str], filas: list[list[object]]) -> None:
    """Muestra una tabla con los datos proporcionados."""
    if not filas:
        mostrar_info("No hay registros para mostrar.")
        return
    CONSOLA.print(crear_tabla(titulo, columnas, filas))

def mostrar_titulo(texto: str) -> None:
    """Muestra un título en amarillo."""
    CONSOLA.print(Text(f"\n{texto}\n", style="bold yellow italic"))

def mostrar_menu(titulo: str, opciones: list[tuple[int, str]]) -> None:
    """Muestra un menú con las opciones proporcionadas."""
    filas = [[numero, texto] for numero, texto in opciones]
    CONSOLA.print(crear_tabla(titulo, ["Opción", "Descripción"], filas, color_encabezado="bold magenta"))

def mostrar_encabezado(texto: str, subtexto: str = "") -> None:
    """Muestra un encabezado con un texto principal y un subtexto opcional."""
    CONSOLA.print(Panel(escape(texto), subtitle=Text(subtexto, style="italic"), style="bold magenta"))

def mostrar_error(mensaje: str) -> None:
    """Muestra un mensaje de error en rojo."""
    CONSOLA.print(f"[bold red]Error:[/] {escape(mensaje)}")

def mostrar_exito(mensaje: str) -> None:
    """Muestra un mensaje de éxito en verde."""
    CONSOLA.print(f"[bold green]OK:[/] {escape(mensaje)}")

def mostrar_info(mensaje: str) -> None:
    """Muestra un mensaje informativo en amarillo."""
    CONSOLA.print(f"[bold yellow]Aviso:[/] {escape(mensaje)}")

def mostrar_sistema(mensaje: str) -> None:
    """Muestra un mensaje del sistema en azul."""
    CONSOLA.print(f"[bold blue]Sistema:[/] {escape(mensaje)}")

def limpiar_consola() -> None:
    """Limpia la consola."""
    CONSOLA.clear()
