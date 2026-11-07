from entidades.base import Base
from entidades.producto import Producto
from excepciones.food_store_error import DatoInvalidoError

class DetallePedido(Base):
    def __init__(self, cantidad: int, producto: Producto) -> None:
        super().__init__()
        self.__producto = producto
        self.__precio_unitario: float = producto.precio
        self.cantidad = cantidad

    @property
    def producto(self) -> Producto:
        return self.__producto

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise DatoInvalidoError("La cantidad debe ser un número entero.")
        elif valor <= 0:
            raise DatoInvalidoError("La cantidad debe ser mayor a cero.")
        self.__cantidad = valor

    @property
    def subtotal(self) -> float:
        return self.cantidad * self.__precio_unitario

    def __str__(self) -> str:
        return f"{self.producto.nombre} x{self.cantidad} - ${self.subtotal}"
