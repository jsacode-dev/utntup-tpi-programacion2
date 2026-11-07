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
        return self.__usuario

    @property
    def fecha(self) -> date:
        return self.__fecha

    @property
    def estado(self) -> Estado:
        return self.__estado

    @property
    def forma_pago(self) -> FormaPago:
        return self.__forma_pago

    @forma_pago.setter
    def forma_pago(self, valor: FormaPago) -> None:
        if not isinstance(valor, FormaPago):
            raise DatoInvalidoError("La forma de pago no es válida.")
        self.__forma_pago = valor

    @property
    def total(self) -> float:
        return self.__total

    @property
    def detalles(self) -> tuple[DetallePedido, ...]:
        return tuple(self.__detalles)

    def cambiar_estado(self, nuevo_estado: Estado) -> None:
        if nuevo_estado not in self.TRANSICIONES[self.__estado]:
            raise OperacionNoPermitidaError(f"No se puede pasar el pedido de {self.__estado.value} a {nuevo_estado.value}.")
        self.__estado = nuevo_estado

    def buscar_detalle_por_producto(self, producto: Producto) -> DetallePedido | None:
        for detalle in self.__detalles:
            if detalle.producto == producto:
                return detalle
        return None

    def agregar_detalle(self, cantidad: int, producto: Producto) -> None:
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
        detalle = self.buscar_detalle_por_producto(producto)
        if detalle is None:
            raise EntidadNoEncontradaError(f"El producto {producto.nombre} no está en el pedido.")
        self.__detalles.remove(detalle)

    def calcular_total(self) -> None:
        self.__total = sum((d.subtotal for d in self.__detalles), 0.0)

    def __str__(self) -> str:
        return f"[{self.id}] {self.fecha} - {self.usuario.nombre} {self.usuario.apellido} - {self.estado.value} - {self.forma_pago.value} - ${self.total}"
