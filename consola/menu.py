from abc import ABC, abstractmethod

from entidades.usuario import Usuario

class Menu(ABC):
    def __init__(self, usuario: Usuario) -> None:
        self._usuario = usuario # Atributo protegido y no privado. Dudoso

    @abstractmethod
    def mostrar(self) -> bool:
        ... # True = cerrar sesión, False = salir del programa
