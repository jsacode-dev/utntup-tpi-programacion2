from entidades.pedido import Pedido
from entidades.usuario import Usuario
from enums.estado import Estado
from enums.forma_pago import FormaPago
from excepciones.food_store_error import DatoInvalidoError, EntidadNoEncontradaError, OperacionNoPermitidaError
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio

class PedidoServicio:
    def __init__(self, usuario_servicio: UsuarioServicio, producto_servicio: ProductoServicio) -> None:
        self.__usuario_servicio = usuario_servicio
        self.__producto_servicio = producto_servicio
        self.__pedidos: list[Pedido] = []

    def listar(self) -> list[Pedido]:
        return [p for p in self.__pedidos if not p.eliminado]

    def listar_de_usuario(self, usuario: Usuario) -> list[Pedido]:
        return [p for p in self.listar() if p.usuario == usuario]

    def buscar_por_id(self, id_pedido: int) -> Pedido:
        for pedido in self.__pedidos:
            if pedido.id == id_pedido and not pedido.eliminado:
                return pedido
        raise EntidadNoEncontradaError(f"Pedido con ID {id_pedido} no encontrado.")

    def buscar_de_usuario(self, id_pedido: int, usuario: Usuario) -> Pedido:
        pedido = self.buscar_por_id(id_pedido)
        if pedido.usuario != usuario:
            raise EntidadNoEncontradaError(f"Pedido con ID {id_pedido} no encontrado.")
        return pedido

    def crear(self, id_usuario: int, forma_pago: FormaPago, items: list[tuple[int, int]]) -> Pedido:
        usuario = self.__usuario_servicio.buscar_por_id(id_usuario)
        if not items:
            raise DatoInvalidoError("El pedido debe tener al menos un producto.")
        pedido = Pedido(usuario, forma_pago) # Todo se valida antes de modificar stock o la colección: Si algo falla, no queda nada guardado.
        for id_producto, cantidad in items:
            producto = self.__producto_servicio.buscar_por_id(id_producto)
            if not producto.disponible: # Regla propia, no figura en la consigna; Se mantiene por ser útil, a confirmar.
                raise OperacionNoPermitidaError(f"El producto {producto.nombre} no está disponible.")
            pedido.agregar_detalle(cantidad, producto)
        pedido.calcular_total()
        for detalle in pedido.detalles:
            detalle.producto.stock -= detalle.cantidad
        self.__pedidos.append(pedido)
        return pedido

    def actualizar(self, id_pedido: int, nuevo_estado: Estado | None = None, nueva_forma_pago: FormaPago | None = None) -> Pedido:
        pedido = self.buscar_por_id(id_pedido)
        if nuevo_estado is not None and nuevo_estado != pedido.estado:
            pedido.cambiar_estado(nuevo_estado)
            if nuevo_estado == Estado.CANCELADO:
                self.__devolver_stock(pedido)
        if nueva_forma_pago is not None:
            pedido.forma_pago = nueva_forma_pago
        return pedido

    def eliminar(self, id_pedido: int) -> None:
        pedido = self.buscar_por_id(id_pedido)
        if pedido.estado not in (Estado.TERMINADO, Estado.CANCELADO):
            self.__devolver_stock(pedido)
        pedido.eliminado = True
        for detalle in pedido.detalles:
            detalle.eliminado = True

    def __devolver_stock(self, pedido: Pedido) -> None:
        for detalle in pedido.detalles:
            detalle.producto.stock += detalle.cantidad
