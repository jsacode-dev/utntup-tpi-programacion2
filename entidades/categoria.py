from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entidades.producto import Producto
from entidades.base import Base
from excepciones.food_store_error import DatoInvalidoError

class Categoria(Base):
    """Representa una categoría de productos."""

    def __init__(self, nombre: str, descripcion: str) -> None:
        super().__init__()
        self.nombre = nombre
        self.descripcion = descripcion
        self.__productos: list[Producto] = []

    @property
    def nombre(self) -> str:
        """Retorna el nombre de la categoría."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Establece el nombre, validando que no esté vacío."""
        if not valor.strip():
            raise DatoInvalidoError("El nombre no puede estar vacío.")
        self.__nombre: str = valor.strip()

    @property
    def descripcion(self) -> str:
        """Retorna la descripción de la categoría."""
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        """Establece la descripción, validando que no esté vacía."""
        if not valor.strip():
            raise DatoInvalidoError("La descripción no puede estar vacía.")
        self.__descripcion: str = valor.strip()

    @property
    def productos(self) -> tuple[Producto, ...]:
        """Retorna una tupla inmutable de los productos de la categoría."""
        return tuple(self.__productos)

    def agregar_producto(self, producto: Producto) -> None:
        """Agrega un producto a la categoría."""
        self.__productos.append(producto)

    def quitar_producto(self, producto: Producto) -> None:
        """Remueve un producto de la categoría."""
        self.__productos.remove(producto)

    def __str__(self) -> str:
        """Devuelve una representación en cadena de la categoría."""
        return f"{self.id} - {self.nombre}: {self.descripcion}"
