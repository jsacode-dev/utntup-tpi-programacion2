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

    def __crear_producto(self) -> None:
        mostrar_tabla("Categorías", ["ID", "Nombre"], [[c.id, c.nombre] for c in self.__categoria_servicio.listar()])
        try:
            nombre = validar_texto("Nombre: ")
            descripcion = validar_texto("Descripción: ")
            precio = validar_numero("Precio: ", decimal = True, no_negativo = True)
            stock = validar_numero("Stock: ", minimo = 0)
            imagen = validar_texto("Imagen (ruta o URL): ")
            disponible = validar_texto("¿Disponible? (S/N): ").upper() == "S"
            id_categoria = validar_numero("ID de categoría: ")
            producto = self.__producto_servicio.crear(nombre, descripcion, precio, stock, imagen, disponible, id_categoria)
            mostrar_exito(f"Producto con ID {producto.id} creado.")
        except FoodStoreError as e:
            mostrar_error(str(e))

    def __editar_producto(self) -> None:
        try:
            id_producto = validar_numero("ID del producto a editar: ")
            actual = self.__producto_servicio.buscar_por_id(id_producto)
            nombre = validar_texto(f"Nombre [{actual.nombre}]: ", salto_valor = True)
            descripcion = validar_texto(f"Descripción [{actual.descripcion}]: ", salto_valor = True)
            precio = validar_numero(f"Precio [{actual.precio}]: ", decimal = True, no_negativo = True, salto_valor = True)
            stock = validar_numero(f"Stock [{actual.stock}]: ", minimo=0, salto_valor = True)
            imagen = validar_texto(f"Imagen [{actual.imagen}]: ", salto_valor = True)
            disponible = validar_texto(f"¿Disponible? (S/N) [{'S' if actual.disponible else 'N'}]: ", salto_valor = True)
            self.__producto_servicio.editar(
                id_producto,
                nombre if nombre is not None else actual.nombre,
                descripcion if descripcion is not None else actual.descripcion,
                precio if precio is not None else actual.precio,
                stock if stock is not None else actual.stock,
                imagen if imagen is not None else actual.imagen,
                disponible.upper() == "S" if disponible is not None else actual.disponible,
            )
            mostrar_exito(f"Producto con ID {id_producto} actualizado.")
        except FoodStoreError as e:
            mostrar_error(str(e))

    def __eliminar_producto(self) -> None:
        try:
            id_producto = validar_numero("ID del producto a eliminar: ")
            if validar_texto("Confirma eliminación? (S/N): ").upper() != "S":
                mostrar_info("Operación cancelada.")
                return
            self.__producto_servicio.eliminar(id_producto)
            mostrar_exito("Producto eliminado.")
        except FoodStoreError as e:
            mostrar_error(str(e))
