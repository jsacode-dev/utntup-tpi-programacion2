from abc import ABC, abstractmethod
from time import sleep
from getpass import getpass

from consola.presentacion import limpiar_consola, mostrar_encabezado, mostrar_error, mostrar_tabla
from consola.validadores import validar_numero, validar_texto
from entidades.categoria import Categoria
from entidades.usuario import Usuario
from excepciones.food_store_error import FoodStoreError
from servicios.categoria_servicio import CategoriaServicio

class Menu(ABC):
    def __init__(self, usuario: Usuario) -> None:
        self._usuario = usuario # Atributo protegido y no privado. Dudoso

    def _nueva_pantalla(self) -> None:
        limpiar_consola()
        mostrar_encabezado("FOOD STORE", f"{self._usuario.rol.value} - {self._usuario.nombre} {self._usuario.apellido}")

    def _pausa(self) -> None:
        sleep(1)

    def _esperar_volver(self) -> None:
        getpass("Presione Enter para volver al menú...") # Se usa getpass para ocultar la entrada del usuario y solo capturar la acción de presionar Enter

    def _elegir_categoria(self, categoria_servicio: CategoriaServicio) -> Categoria | None:
        if (validar_texto("¿Filtrar por categoría? (S/N): ") or "").upper() != "S":
            return None
        mostrar_tabla("Categorías", ["ID", "Nombre"], [[c.id, c.nombre] for c in categoria_servicio.listar()])
        while True:
            try:
                return categoria_servicio.buscar_por_id(int(validar_numero("ID de la categoría: ")))
            except FoodStoreError as e:
                mostrar_error(str(e))

    @abstractmethod
    def mostrar(self) -> bool:
        ... # True = cerrar sesión, False = salir del programa
