from entidades.base import Base
from entidades.producto import Producto
from excepciones.food_store_error import DatoInvalidoError

class DetallePedido(Base):
    """Representa un detalle de un producto dentro de un pedido."""

    def __init__(self, cantidad: int, producto: Producto) -> None:
        super().__init__()
        self.__producto = producto
        self.__precio_unitario: float = producto.precio
        self.cantidad = cantidad

    @property
    def producto(self) -> Producto:
        """Retorna el producto asociado al detalle del pedido."""
        return self.__producto

    @property
    def cantidad(self) -> int:
        """Retorna la cantidad de productos en el detalle del pedido."""
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        """Establece la cantidad, validando que sea un entero positivo."""
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise DatoInvalidoError("La cantidad debe ser un número entero.")
        elif valor <= 0:
            raise DatoInvalidoError("La cantidad debe ser mayor a cero.")
        self.__cantidad = valor

    @property
    def subtotal(self) -> float:
        """Calcula el subtotal del detalle (cantidad × precio unitario)."""
        return self.cantidad * self.__precio_unitario

    def __str__(self) -> str:
        """Devuelve una representación en cadena del detalle del pedido."""
        return f"{self.producto.nombre} x{self.cantidad} - ${self.subtotal}"
