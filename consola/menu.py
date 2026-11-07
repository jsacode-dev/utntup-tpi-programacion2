from abc import ABC, abstractmethod
from time import sleep
from getpass import getpass

from consola.presentacion import limpiar_consola, mostrar_encabezado
from entidades.usuario import Usuario

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

    @abstractmethod
    def mostrar(self) -> bool:
        ... # True = cerrar sesión, False = salir del programa
