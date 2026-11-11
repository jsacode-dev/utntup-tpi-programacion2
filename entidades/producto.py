from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entidades.categoria import Categoria
from entidades.base import Base
from excepciones.food_store_error import DatoInvalidoError, PrecioInvalidoError

class Producto(Base):
    """Representa un producto con precio, stock y disponibilidad."""

    def __init__(self, nombre: str, descripcion: str, precio: float, stock: int, imagen: str, disponible: bool, categoria: Categoria) -> None:
        super().__init__()
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.imagen = imagen
        self.disponible = disponible
        self.__categoria = categoria
        categoria.agregar_producto(self)

    @property
    def nombre(self) -> str:
        """Retorna el nombre del producto."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Establece el nombre, validando que no esté vacío."""
        if not valor.strip():
            raise DatoInvalidoError("El nombre no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def descripcion(self) -> str:
        """Retorna la descripción del producto."""
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        """Establece la descripción, validando que no esté vacía."""
        if not valor.strip():
            raise DatoInvalidoError("La descripción no puede estar vacía.")
        self.__descripcion: str = valor.strip()

    @property
    def precio(self) -> float:
        """Retorna el precio del producto."""
        return self.__precio

    @precio.setter
    def precio(self, valor: float) -> None:
        """Establece el precio, validando que sea un número positivo."""
        if not isinstance(valor, (int, float)) or isinstance(valor, bool):
            raise PrecioInvalidoError("El precio debe ser un número.")
        elif valor < 0:
            raise PrecioInvalidoError("El precio no puede ser negativo.")
        self.__precio = valor

    @property
    def stock(self) -> int:
        """Retorna el stock del producto."""
        return self.__stock

    @stock.setter
    def stock(self, valor: int) -> None:
        """Establece el stock, validando que sea un entero no negativo."""
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise DatoInvalidoError("El stock debe ser un número entero.")
        elif valor < 0:
            raise DatoInvalidoError("El stock no puede ser negativo.")
        self.__stock = valor

    @property
    def imagen(self) -> str:
        """Retorna la URL de la imagen del producto."""
        return self.__imagen

    @imagen.setter
    def imagen(self, valor: str) -> None:
        """Establece la imagen, validando que no esté vacía."""
        if not valor.strip():
            raise DatoInvalidoError("La imagen no puede estar vacía.")
        self.__imagen = valor.strip()

    @property
    def disponible(self) -> bool:
        """Retorna si el producto está disponible."""
        return self.__disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        """Establece la disponibilidad del producto."""
        if not isinstance(valor, bool):
            raise DatoInvalidoError("El valor de disponible debe ser un booleano.")
        self.__disponible = valor

    @property
    def categoria(self) -> Categoria:
        """Retorna la categoría a la que pertenece el producto."""
        return self.__categoria

    def __str__(self) -> str:
        """Retorna una representación en cadena del producto."""
        return f"[{self.id}] {self.nombre} - ${self.precio} (Stock: {self.stock})"
