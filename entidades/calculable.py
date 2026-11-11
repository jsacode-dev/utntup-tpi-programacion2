from abc import ABC, abstractmethod

class Calculable(ABC):
    """Interfaz para objetos con total calculable."""

    @abstractmethod
    def calcular_total(self) -> None:
        """Calcula el total de un objeto que implementa esta interfaz."""
        ...
