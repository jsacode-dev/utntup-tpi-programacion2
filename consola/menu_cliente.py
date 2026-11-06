from consola.menu import Menu
from consola.presentacion import mostrar_encabezado, mostrar_error, mostrar_info, mostrar_menu, mostrar_tabla
from consola.validadores import validar_numero
from entidades.usuario import Usuario
from servicios.producto_servicio import ProductoServicio

class MenuCliente(Menu):
    def __init__(self, usuario: Usuario, producto_servicio: ProductoServicio) -> None:
        super().__init__(usuario)
        self.__producto_servicio = producto_servicio

    def mostrar(self) -> bool:
        while True:
            mostrar_encabezado("FOOD STORE (CLIENTE)", f"{self._usuario.nombre} {self._usuario.apellido}")
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
                    mostrar_tabla("Productos disponibles", ["ID", "Nombre", "Precio", "Stock"], [
                        [p.id, p.nombre, p.precio, p.stock] for p in self.__producto_servicio.listar_disponibles()
                    ])
                case 1 | 3 | 4:
                    mostrar_info("Módulo en desarrollo.")
                case 9:
                    return True
                case 0:
                    return False
                case _:
                    mostrar_error("Opción inexistente, intente nuevamente.")
