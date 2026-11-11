from abc import ABC, abstractmethod
from datetime import datetime

class Base(ABC):
    """Clase base para todas las entidades con ID único y estado de eliminación."""

    _contador: int = 0

    def __init__(self) -> None:
        self.__id: int = Base._contador
        Base._contador += 1
        self.__eliminado: bool = False
        self.__creado_en: datetime = datetime.now()

    @property
    def id(self) -> int:
        """Retorna el ID único de la entidad."""
        return self.__id

    @property
    def eliminado(self) -> bool:
        """Indica si la entidad ha sido marcada como eliminada."""
        return self.__eliminado

    @eliminado.setter
    def eliminado(self, valor: bool) -> None:
        """Marca o desmarca la entidad como eliminada."""
        self.__eliminado = valor

    @property
    def creado_en(self) -> datetime:
        """Retorna la fecha y hora de creación de la entidad."""
        return self.__creado_en

    def __eq__(self, otro: object) -> bool:
        """Compara dos entidades por su ID."""
        if not isinstance(otro, Base):
            return False
        return self.id == otro.id

    @abstractmethod
    def __str__(self) -> str:
        """Devuelve una representación en cadena de la entidad."""
        ...
