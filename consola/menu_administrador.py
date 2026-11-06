from consola.menu import Menu
from consola.presentacion import mostrar_encabezado, mostrar_error, mostrar_exito, mostrar_info, mostrar_menu, mostrar_tabla
from consola.validadores import validar_numero, validar_texto
from entidades.usuario import Usuario
from excepciones.food_store_error import FoodStoreError
from servicios.categoria_servicio import CategoriaServicio
from servicios.producto_servicio import ProductoServicio

class MenuAdministrador(Menu):
    def __init__(self, usuario: Usuario, categoria_servicio: CategoriaServicio, producto_servicio: ProductoServicio) -> None:
        super().__init__(usuario)
        self.__categoria_servicio = categoria_servicio
        self.__producto_servicio = producto_servicio

    def mostrar(self) -> bool:
        while True:
            mostrar_encabezado("FOOD STORE (ADMINISTRADOR)", f"{self._usuario.nombre} {self._usuario.apellido}")
            mostrar_menu("Menú principal", [
                (1, "Categorías"),
                (2, "Productos"),
                (3, "Usuarios"),
                (4, "Pedidos"),
                (9, "Cerrar sesión"),
                (0, "Salir"),
            ])
            opcion = validar_numero("Seleccione una opción: ", minimo = 0, maximo = 9)

            match opcion:
                case 2:
                    self.__menu_productos()
                case 1 | 3 | 4:
                    mostrar_info("Módulo en desarrollo.")
                case 9:
                    return True
                case 0:
                    return False
                case _:
                    mostrar_error("Opción inexistente, intente nuevamente.")

    def __menu_productos(self) -> None:
        while True:
            mostrar_menu("Productos", [(1, "Listar"), (2, "Crear"), (3, "Editar"), (4, "Eliminar"), (0, "Volver")])
            opcion = validar_numero("Seleccione una opción: ", minimo = 0, maximo = 4)

            match opcion:
                case 1:
                    mostrar_tabla("Productos", ["ID", "Nombre", "Precio", "Stock", "Categoría"], [
                        [p.id, p.nombre, p.precio, p.stock, p.categoria.nombre] for p in self.__producto_servicio.listar()
                    ])
                case 2:
                    self.__crear_producto()
                case 3:
                    self.__editar_producto()
                case 4:
                    self.__eliminar_producto()
                case 0:
                    return

# Falta __crear_producto, __editar_producto y __eliminar_producto
# Falta hacer este proceso en menu_cliente.py
# Falta cambiar la consulta del rol en main.py
