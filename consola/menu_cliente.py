from consola.menu import Menu
from consola.presentacion import mostrar_error, mostrar_info, mostrar_menu, mostrar_tabla
from consola.validadores import validar_numero
from entidades.usuario import Usuario
from excepciones.food_store_error import FoodStoreError
from servicios.pedido_servicio import PedidoServicio
from servicios.producto_servicio import ProductoServicio

class MenuCliente(Menu):
    def __init__(self, usuario: Usuario, producto_servicio: ProductoServicio, pedido_servicio: PedidoServicio) -> None:
        super().__init__(usuario)
        self.__producto_servicio = producto_servicio
        self.__pedido_servicio = pedido_servicio

    def mostrar(self) -> bool:
        while True:
            self._nueva_pantalla()
            mostrar_menu("Menú principal", [
                (1, "Ver categorías"),
                (2, "Ver productos disponibles"),
                (3, "Mis pedidos"),
                (4, "Mis datos"),
                (9, "Cerrar sesión"),
                (0, "Salir"),
            ])
            opcion = validar_numero("Seleccione una opción: ", minimo = 0, maximo = 9)

            match opcion:
                case 2:
                    self.__productos_disponibles()
                case 4:
                    self.__mis_datos()
                case 3:
                    self.__mis_pedidos()
                case 1:
                    mostrar_info("Módulo en desarrollo.")
                    self._pausa()
                case 9:
                    return True
                case 0:
                    return False
                case _:
                    mostrar_error("Opción inexistente, intente nuevamente.")
                    self._pausa()

    def __productos_disponibles(self) -> None:
        self._nueva_pantalla()
        productos = self.__producto_servicio.listar_disponibles()
        if not productos:
            mostrar_info("No hay productos disponibles para mostrar.")
            self._pausa()
            return
        mostrar_tabla("Productos disponibles", ["ID", "Nombre", "Precio", "Stock"], [
            [p.id, p.nombre, p.precio, p.stock] for p in productos
        ])
        self._esperar_volver()

    def __mis_datos(self) -> None:
        self._nueva_pantalla()
        mostrar_tabla("Mis datos", ["Nombre", "Apellido", "Mail", "Celular", "Rol"], [
            [self._usuario.nombre, self._usuario.apellido, self._usuario.mail, self._usuario.celular, self._usuario.rol.value]
        ])
        self._esperar_volver()

    def __mis_pedidos(self) -> None:
        self._nueva_pantalla()
        pedidos = self.__pedido_servicio.listar_de_usuario(self._usuario)
        if not pedidos:
            mostrar_info("No tiene pedidos registrados.")
            self._pausa()
            return
        mostrar_tabla("Mis pedidos", ["ID", "Estado", "Forma de pago", "Total", "Fecha"], [
            [p.id, p.estado.value, p.forma_pago.value, p.total, p.fecha] for p in pedidos
        ])
        id_pedido = validar_numero("ID del pedido para ver el detalle (0 para volver): ", minimo = 0)
        if id_pedido == 0:
            return
        try:
            pedido = self.__pedido_servicio.buscar_de_usuario(id_pedido, self._usuario)
            mostrar_tabla(f"Detalle del pedido {pedido.id}", ["Producto", "Cantidad", "Subtotal"], [
                [d.producto.nombre, d.cantidad, d.subtotal] for d in pedido.detalles
            ])
            mostrar_info(f"Total: ${pedido.total}")
        except FoodStoreError as e:
            mostrar_error(str(e))
        self._esperar_volver()
