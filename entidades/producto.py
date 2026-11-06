from entidades.base import Base
from entidades.categoria import Categoria
from excepciones.food_store_error import DatoInvalidoError, PrecioInvalidoError

class Producto(Base):
    def __init__(self, nombre: str, descripcion: str, precio: float, stock: int, imagen: str, disponible: bool, categoria: Categoria) -> None:
        super().__init__()
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.imagen = imagen
        self.disponible = disponible
        self.categoria = categoria
        categoria.agregar_producto(self)

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor.strip():
            raise DatoInvalidoError("El nombre no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        if not valor.strip():
            raise DatoInvalidoError("La descripción no puede estar vacía.")
        self.__descripcion: str = valor.strip()

    @property
    def precio(self) -> float:
        return self.__precio

    @precio.setter
    def precio(self, valor: float) -> None:
        if not isinstance(valor, (int, float)) or isinstance(valor, bool):
            raise PrecioInvalidoError("El precio debe ser un número.")
        elif valor < 0:
            raise PrecioInvalidoError("El precio no puede ser negativo.")
        self.__precio = valor

    @property
    def stock(self) -> int:
        return self.__stock

    @stock.setter
    def stock(self, valor: int) -> None:
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise DatoInvalidoError("El stock debe ser un número entero.")
        self.__stock = valor

    @property
    def imagen(self) -> str:
        return self.__imagen

    @imagen.setter
    def imagen(self, valor: str) -> None:
        if not valor.strip():
            raise DatoInvalidoError("La imagen no puede estar vacía.")
        self.__imagen = valor.strip()

    @property
    def disponible(self) -> bool:
        return self.__disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise DatoInvalidoError("El valor de disponible debe ser un booleano.")
        self.__disponible = valor

    @property
    def categoria(self) -> Categoria:
        return self.__categoria

    def __str__(self) -> str:
        return f"[{self.id}] {self.nombre} - ${self.precio} (Stock: {self.stock})"
