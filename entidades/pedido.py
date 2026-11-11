from datetime import date

from entidades.base import Base
from entidades.calculable import Calculable
from entidades.detalle_pedido import DetallePedido
from entidades.producto import Producto
from entidades.usuario import Usuario
from enums.estado import Estado
from enums.forma_pago import FormaPago
from excepciones.food_store_error import DatoInvalidoError, EntidadNoEncontradaError, OperacionNoPermitidaError, StockInsuficienteError

class Pedido(Base, Calculable):
    """Representa un pedido con detalles de productos y transiciones de estado."""

    """Define las transiciones de estado permitidas para un pedido."""
    TRANSICIONES: dict[Estado, set[Estado]] = {
        Estado.PENDIENTE: {Estado.CONFIRMADO, Estado.CANCELADO},
        Estado.CONFIRMADO: {Estado.TERMINADO, Estado.CANCELADO},
        Estado.TERMINADO: set(),
        Estado.CANCELADO: set(),
    }

    def __init__(self, usuario: Usuario, forma_pago: FormaPago) -> None:
        super().__init__()
        self.__usuario = usuario
        self.forma_pago = forma_pago
        self.__fecha: date = date.today()
        self.__estado: Estado = Estado.PENDIENTE
        self.__total: float = 0.0
        self.__detalles: list[DetallePedido] = []

    @property
    def usuario(self) -> Usuario:
        """Retorna el usuario que realizó el pedido."""
        return self.__usuario

    @property
    def fecha(self) -> date:
        """Retorna la fecha del pedido."""
        return self.__fecha

    @property
    def estado(self) -> Estado:
        """Retorna el estado actual del pedido."""
        return self.__estado

    @property
    def forma_pago(self) -> FormaPago:
        """Retorna la forma de pago del pedido."""
        return self.__forma_pago

    @forma_pago.setter
    def forma_pago(self, valor: FormaPago) -> None:
        """Establece la forma de pago del pedido, validando su tipo."""
        if not isinstance(valor, FormaPago):
            raise DatoInvalidoError("La forma de pago no es válida.")
        self.__forma_pago = valor

    @property
    def total(self) -> float:
        """Retorna el total del pedido."""
        return self.__total

    @property
    def detalles(self) -> tuple[DetallePedido, ...]:
        """Retorna una tupla inmutable de los detalles del pedido."""
        return tuple(self.__detalles)

    def cambiar_estado(self, nuevo_estado: Estado) -> None:
        """Cambia el estado del pedido validando transiciones permitidas."""
        if nuevo_estado not in self.TRANSICIONES[self.__estado]:
            raise OperacionNoPermitidaError(f"No se puede pasar el pedido de {self.__estado.value} a {nuevo_estado.value}.")
        self.__estado = nuevo_estado

    def buscar_detalle_por_producto(self, producto: Producto) -> DetallePedido | None:
        """Busca un detalle en el pedido por producto."""
        for detalle in self.__detalles:
            if detalle.producto == producto:
                return detalle
        return None

    def agregar_detalle(self, cantidad: int, producto: Producto) -> None:
        """Agrega un detalle al pedido, validando stock disponible."""
        if not isinstance(cantidad, int) or isinstance(cantidad, bool):
            raise DatoInvalidoError("La cantidad debe ser un número entero.")
        elif cantidad <= 0:
            raise DatoInvalidoError("La cantidad debe ser mayor a cero.")
        detalle = self.buscar_detalle_por_producto(producto)
        cantidad_total = cantidad + (detalle.cantidad if detalle is not None else 0)
        if cantidad_total > producto.stock:
            raise StockInsuficienteError(f"Stock insuficiente de {producto.nombre}. Disponible: {producto.stock}.")
        if detalle is None:
            self.__detalles.append(DetallePedido(cantidad, producto))
        else:
            detalle.cantidad = cantidad_total

    def eliminar_detalle_por_producto(self, producto: Producto) -> None:
        """Elimina un detalle del pedido por producto."""
        detalle = self.buscar_detalle_por_producto(producto)
        if detalle is None:
            raise EntidadNoEncontradaError(f"El producto {producto.nombre} no está en el pedido.")
        self.__detalles.remove(detalle)

    def calcular_total(self) -> None:
        """Calcula el total del pedido sumando los subtotales de los detalles."""
        self.__total = sum((d.subtotal for d in self.__detalles), 0.0)

    def __str__(self) -> str:
        """Devuelve una representación en cadena del pedido."""
        return f"[{self.id}] {self.fecha} - {self.usuario.nombre} {self.usuario.apellido} - {self.estado.value} - {self.forma_pago.value} - ${self.total}"
