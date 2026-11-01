from consola.menu import Menu
from consola.presentacion import mostrar_encabezado, mostrar_error, mostrar_info, mostrar_menu
from consola.validadores import validar_numero

class MenuAdministrador(Menu):
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
            opcion = validar_numero("Seleccione una opción: ", minimo=0, maximo=9)
            if opcion in (1, 2, 3, 4):
                mostrar_info("Módulo en desarrollo.")
            elif opcion == 9:
                return True
            elif opcion == 0:
                return False
            else:
                mostrar_error("Opción inexistente, intente nuevamente.")
