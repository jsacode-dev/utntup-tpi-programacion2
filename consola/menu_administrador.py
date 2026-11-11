from collections.abc import Sequence
from enum import Enum
from getpass import getpass

from consola.menu import Menu
from consola.presentacion import mostrar_error, mostrar_exito, mostrar_info, mostrar_menu, mostrar_tabla, mostrar_titulo
from consola.validadores import validar_email, validar_numero, validar_texto
from entidades.usuario import Usuario
from enums.estado import Estado
from enums.forma_pago import FormaPago
from enums.rol import Rol
from excepciones.food_store_error import FoodStoreError
from servicios.categoria_servicio import CategoriaServicio
from servicios.pedido_servicio import PedidoServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio

class MenuAdministrador(Menu):
    """Menú de administrador con acceso a categorías, productos, usuarios y pedidos."""

    def __init__(self, usuario: Usuario, categoria_servicio: CategoriaServicio, producto_servicio: ProductoServicio, usuario_servicio: UsuarioServicio, pedido_servicio: PedidoServicio) -> None:
        super().__init__(usuario)
        self.__categoria_servicio = categoria_servicio
        self.__producto_servicio = producto_servicio
        self.__usuario_servicio = usuario_servicio
        self.__pedido_servicio = pedido_servicio

    def mostrar(self) -> bool:
        """Muestra el menú principal del administrador."""
        while True:
            self._nueva_pantalla()
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
                case 3:
                    self.__menu_usuarios()
                case 4:
                    self.__menu_pedidos()
                case 1:
                    self.__menu_categorias()
                case 9:
                    return True
                case 0:
                    return False
                case _:
                    mostrar_error("Opción inexistente, intente nuevamente.")
                    self._pausa()

    def __sin_registros(self, registros: Sequence[object], mensaje: str) -> bool:
        """Verifica si no hay registros y muestra un mensaje informativo."""
        if registros:
            return False
        mostrar_info(mensaje)
        self._pausa()
        return True

    def __menu_categorias(self) -> None:
        """Muestra el menú de categorías y gestiona las acciones del administrador."""
        while True:
            self._nueva_pantalla()
            mostrar_menu("Categorías", [(1, "Listar"), (2, "Crear"), (3, "Editar"), (4, "Eliminar"), (0, "Volver")])
            opcion = validar_numero("Seleccione una opción: ", minimo = 0, maximo = 4)

            match opcion:
                case 1:
                    self.__listar_categorias()
                case 2:
                    mostrar_titulo("Crear categoría")
                    self.__crear_categoria()
                    self._pausa()
                case 3:
                    if self.__sin_registros(self.__categoria_servicio.listar(), "No hay categorías para editar."):
                        continue
                    mostrar_titulo("Editar categoría")
                    self.__editar_categoria()
                    self._pausa()
                case 4:
                    if self.__sin_registros(self.__categoria_servicio.listar(), "No hay categorías para eliminar."):
                        continue
                    mostrar_titulo("Eliminar categoría")
                    self.__eliminar_categoria()
                    self._pausa()
                case 0:
                    return

    def __mostrar_categorias(self) -> None:
        """Muestra todas las categorías en una tabla."""
        mostrar_tabla("Categorías", ["ID", "Nombre", "Descripción"], [
            [c.id, c.nombre, c.descripcion] for c in self.__categoria_servicio.listar()
        ])

    def __listar_categorias(self) -> None:
        """Lista todas las categorías disponibles."""
        self._nueva_pantalla()
        if not self.__categoria_servicio.listar():
            mostrar_info("No hay categorías cargadas")
            self._pausa()
            return
        self.__mostrar_categorias()
        self._esperar_volver()

    def __crear_categoria(self) -> None:
        """Crea una nueva categoría."""
        try:
            nombre = validar_texto("Nombre: ")
            descripcion = validar_texto("Descripción: ")
            categoria = self.__categoria_servicio.crear(nombre, descripcion)
            mostrar_exito(f"Categoría con ID {categoria.id} creada.")
        except FoodStoreError as e:
            mostrar_error(str(e))

    def __editar_categoria(self) -> None:
        """Edita una categoría existente."""
        try:
            self.__mostrar_categorias()
            id_categoria = validar_numero("ID de la categoría a editar: ")
            actual = self.__categoria_servicio.buscar_por_id(id_categoria)
            nombre = validar_texto(f"Nombre [{actual.nombre}]: ", salto_valor = True)
            descripcion = validar_texto(f"Descripción [{actual.descripcion}]: ", salto_valor = True)
            self.__categoria_servicio.editar(
                id_categoria,
                nombre if nombre is not None else actual.nombre,
                descripcion if descripcion is not None else actual.descripcion,
            )
            mostrar_exito(f"Categoría con ID {id_categoria} actualizada.")
        except FoodStoreError as e:
            mostrar_error(str(e))

    def __eliminar_categoria(self) -> None:
        """Elimina una categoría existente."""
        try:
            self.__mostrar_categorias()
            id_categoria = validar_numero("ID de la categoría a eliminar: ")
            self.__categoria_servicio.buscar_por_id(id_categoria)
            if validar_texto("Confirma eliminación? (S/N): ").upper() != "S":
                mostrar_info("Operación cancelada.")
                return
            self.__categoria_servicio.eliminar(id_categoria)
            mostrar_exito("Categoría eliminada.")
        except FoodStoreError as e:
            mostrar_error(str(e))

    def __menu_productos(self) -> None:
        """Muestra el menú de productos y gestiona las acciones del administrador."""
        while True:
            self._nueva_pantalla()
            mostrar_menu("Productos", [(1, "Listar"), (2, "Crear"), (3, "Editar"), (4, "Eliminar"), (0, "Volver")])
            opcion = validar_numero("Seleccione una opción: ", minimo = 0, maximo = 4)

            match opcion:
                case 1:
                    self.__listar_productos()
                case 2:
                    mostrar_titulo("Crear producto")
                    self.__crear_producto()
                    self._pausa()
                case 3:
                    if self.__sin_registros(self.__producto_servicio.listar(), "No hay productos para editar."):
                        continue
                    mostrar_titulo("Editar producto")
                    self.__editar_producto()
                    self._pausa()
                case 4:
                    if self.__sin_registros(self.__producto_servicio.listar(), "No hay productos para eliminar."):
                        continue
                    mostrar_titulo("Eliminar producto")
                    self.__eliminar_producto()
                    self._pausa()
                case 0:
                    return

    def __listar_productos(self) -> None:
        """Lista todos los productos, opcionalmente filtrados por categoría."""
        self._nueva_pantalla()
        categoria = self._elegir_categoria(self.__categoria_servicio)
        productos = self.__producto_servicio.listar(categoria)
        if not productos:
            mostrar_info("No hay productos registrados.")
            self._pausa()
            return
        mostrar_tabla("Productos", ["ID", "Nombre", "Precio", "Stock", "Categoría"], [
            [p.id, p.nombre, p.precio, p.stock, p.categoria.nombre] for p in productos
        ])
        self._esperar_volver()

    def __menu_usuarios(self) -> None:
        """Muestra el menú de usuarios y gestiona las acciones del administrador."""
        while True:
            self._nueva_pantalla()
            mostrar_menu("Usuarios", [(1, "Listar"), (2, "Crear"), (3, "Editar"), (4, "Eliminar"), (0, "Volver")])
            opcion = validar_numero("Seleccione una opción: ", minimo = 0, maximo = 4)

            match opcion:
                case 1:
                    self.__listar_usuarios()
                case 2:
                    mostrar_titulo("Crear usuario")
                    self.__crear_usuario()
                    self._pausa()
                case 3:
                    if self.__sin_registros(self.__usuario_servicio.listar(), "No hay usuarios para editar."):
                        continue
                    mostrar_titulo("Editar usuario")
                    self.__editar_usuario()
                    self._pausa()
                case 4:
                    if self.__sin_registros(self.__usuario_servicio.listar(), "No hay usuarios para eliminar."):
                        continue
                    mostrar_titulo("Eliminar usuario")
                    self.__eliminar_usuario()
                    self._pausa()
                case 0:
                    return

    def __listar_usuarios(self) -> None:
        """Lista todos los usuarios registrados."""
        self._nueva_pantalla()
        usuarios = self.__usuario_servicio.listar()
        if not usuarios:
            mostrar_info("No hay usuarios registrados.")
            self._pausa()
            return
        mostrar_tabla("Usuarios", ["ID", "Nombre", "Apellido", "Mail", "Rol"], [
            [u.id, u.nombre, u.apellido, u.mail, u.rol.value] for u in usuarios
        ])
        self._esperar_volver()

    def __pedir_enum(self, titulo: str, enumerado: type[Enum], actual: Enum | None = None) -> Enum | None:
        """Solicita al usuario que elija un valor de un enumerado, opcionalmente mostrando el valor actual."""
        opciones_enum = list(enumerado)
        opciones = ", ".join(f"{i} = {op.value}" for i, op in enumerate(opciones_enum, 1))
        texto_actual = f" [{actual.value}]" if actual is not None else ""
        numero = validar_numero(f"{titulo}{texto_actual} ({opciones}): ", minimo = 1, maximo = len(opciones_enum), salto_valor = actual is not None)
        return opciones_enum[int(numero) - 1] if numero is not None else None

    def __pedir_mail_nuevo(self) -> str:
        """Solicita un mail nuevo que no esté registrado en el sistema."""
        while True:
            mail = validar_email("Mail: ")
            if self.__usuario_servicio.mail_disponible(mail):
                return mail
            mostrar_error("Ya existe un usuario con ese mail.")

    def __crear_usuario(self) -> None:
        """Crea un nuevo usuario en el sistema."""
        try:
            nombre = validar_texto("Nombre: ")
            apellido = validar_texto("Apellido: ")
            mail = self.__pedir_mail_nuevo()
            celular = validar_texto("Celular: ")
            contrasenia = getpass("Contraseña: ")
            usuario = self.__usuario_servicio.crear(nombre, apellido, mail, celular, contrasenia, self.__pedir_enum("Rol", Rol))
            mostrar_exito(f"Usuario con ID {usuario.id} creado.")
        except FoodStoreError as e:
            mostrar_error(str(e))

    def __editar_usuario(self) -> None:
        """Edita un usuario existente."""
        try:
            id_usuario = validar_numero("ID del usuario a editar: ")
            actual = self.__usuario_servicio.buscar_por_id(id_usuario)
            nombre = validar_texto(f"Nombre [{actual.nombre}]: ", salto_valor = True)
            apellido = validar_texto(f"Apellido [{actual.apellido}]: ", salto_valor = True)
            mail = validar_email(f"Mail [{actual.mail}]: ", salto_valor = True)
            celular = validar_texto(f"Celular [{actual.celular}]: ", salto_valor = True)
            es_propio = id_usuario == self._usuario.id
            rol = None if es_propio else self.__pedir_enum("Rol", Rol, actual.rol)
            self.__usuario_servicio.editar(
                id_usuario,
                self._usuario.id,
                nombre if nombre is not None else actual.nombre,
                apellido if apellido is not None else actual.apellido,
                mail if mail is not None else actual.mail,
                celular if celular is not None else actual.celular,
                rol if rol is not None else actual.rol,
            )
            mostrar_exito(f"Usuario con ID {id_usuario} actualizado.")
        except FoodStoreError as e:
            mostrar_error(str(e))

    def __eliminar_usuario(self) -> None:
        """Elimina un usuario existente."""
        try:
            id_usuario = validar_numero("ID del usuario a eliminar: ")
            if validar_texto("Confirma eliminación? (S/N): ").upper() != "S":
                mostrar_info("Operación cancelada.")
                return
            self.__usuario_servicio.eliminar(id_usuario, self._usuario.id)
            mostrar_exito("Usuario eliminado.")
        except FoodStoreError as e:
            mostrar_error(str(e))

    def __crear_producto(self) -> None:
        """Crea un nuevo producto en el sistema."""
        categorias = self.__categoria_servicio.listar()
        if not categorias:
            mostrar_info("No hay categorías registradas. Cree una categoría antes de crear un producto.")
            self._pausa()
            return
        mostrar_tabla("Categorías", ["ID", "Nombre"], [[c.id, c.nombre] for c in categorias])
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
        """Edita un producto existente."""
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
        """Elimina un producto existente."""
        try:
            id_producto = validar_numero("ID del producto a eliminar: ")
            if validar_texto("Confirma eliminación? (S/N): ").upper() != "S":
                mostrar_info("Operación cancelada.")
                return
            self.__producto_servicio.eliminar(id_producto)
            mostrar_exito("Producto eliminado.")
        except FoodStoreError as e:
            mostrar_error(str(e))

    def __menu_pedidos(self) -> None:
        """Muestra el menú de gestión de pedidos."""
        while True:
            self._nueva_pantalla()
            mostrar_menu("Pedidos", [(1, "Listar"), (2, "Crear"), (3, "Actualizar estado / forma de pago"), (4, "Eliminar"), (0, "Volver")])
            opcion = validar_numero("Seleccione una opción: ", minimo = 0, maximo = 4)

            match opcion:
                case 1:
                    self.__listar_pedidos()
                case 2:
                    mostrar_titulo("Crear pedido")
                    self.__crear_pedido()
                    self._pausa()
                case 3:
                    if self.__sin_registros(self.__pedido_servicio.listar(), "No hay pedidos para actualizar."):
                        continue
                    mostrar_titulo("Actualizar pedido")
                    self.__actualizar_pedido()
                    self._pausa()
                case 4:
                    if self.__sin_registros(self.__pedido_servicio.listar(), "No hay pedidos para eliminar."):
                        continue
                    mostrar_titulo("Eliminar pedido")
                    self.__eliminar_pedido()
                    self._pausa()
                case 0:
                    return

    def __listar_pedidos(self) -> None:
        """Lista los pedidos de un usuario específico."""
        self._nueva_pantalla()
        usuario = self.__elegir_usuario()
        pedidos = self.__pedido_servicio.listar(usuario)
        if not pedidos:
            mostrar_info("No hay pedidos registrados.")
            self._pausa()
            return
        mostrar_tabla("Pedidos", ["ID", "Usuario", "Estado", "Forma de pago", "Total", "Fecha"], [
            [p.id, f"{p.usuario.nombre} {p.usuario.apellido}", p.estado.value, p.forma_pago.value, p.total, p.fecha] for p in pedidos
        ])
        id_pedido = validar_numero("ID del pedido para ver el detalle (Enter para volver): ", salto_valor = True)
        if id_pedido is not None:
            try:
                pedido = self.__pedido_servicio.buscar_por_id(int(id_pedido))
                mostrar_tabla(f"Detalle del pedido {pedido.id}", ["Producto", "Cantidad", "Subtotal"], [
                    [d.producto.nombre, d.cantidad, d.subtotal] for d in pedido.detalles
                ])
                mostrar_info(f"Total: ${pedido.total}")
            except FoodStoreError as e:
                mostrar_error(str(e))
        self._esperar_volver()

    def __elegir_usuario(self) -> Usuario | None:
        """Permite seleccionar un usuario de la lista o filtrar por usuario."""
        if (validar_texto("¿Filtrar por usuario? (S/N): ") or "").upper() != "S":
            return None
        mostrar_tabla("Usuarios", ["ID", "Nombre", "Apellido", "Mail"], [
            [u.id, u.nombre, u.apellido, u.mail] for u in self.__usuario_servicio.listar()
        ])
        while True:
            try:
                return self.__usuario_servicio.buscar_por_id(int(validar_numero("ID del usuario: ")))
            except FoodStoreError as e:
                mostrar_error(str(e))

    def __crear_pedido(self) -> None:
        """Crea un nuevo pedido para un usuario seleccionado."""
        disponibles = self.__producto_servicio.listar_disponibles()
        if not disponibles:
            mostrar_info("No hay productos disponibles con stock para crear un pedido.")
            return
        try:
            mostrar_tabla("Usuarios", ["ID", "Nombre", "Apellido", "Mail"], [
                [u.id, u.nombre, u.apellido, u.mail] for u in self.__usuario_servicio.listar()
            ])
            id_usuario = validar_numero("ID del usuario: ")
            forma_pago = self.__pedir_enum("Forma de pago", FormaPago)
            mostrar_tabla("Productos disponibles", ["ID", "Nombre", "Precio", "Stock"], [
                [p.id, p.nombre, p.precio, p.stock] for p in disponibles
            ])
            items: list[tuple[int, int]] = []
            while True:
                id_producto = validar_numero("ID del producto: ")
                cantidad = validar_numero("Cantidad: ", minimo = 1)
                items.append((id_producto, cantidad))
                if validar_texto("¿Agregar otro producto? (S/N): ").upper() != "S":
                    break
            pedido = self.__pedido_servicio.crear(id_usuario, forma_pago, items)
            mostrar_exito(f"Pedido con ID {pedido.id} creado. Total: ${pedido.total}.")
        except FoodStoreError as e:
            mostrar_error(str(e))

    def __actualizar_pedido(self) -> None:
        """Actualiza el estado y la forma de pago de un pedido existente."""
        try:
            id_pedido = validar_numero("ID del pedido a actualizar: ")
            actual = self.__pedido_servicio.buscar_por_id(id_pedido)
            nuevo_estado = self.__pedir_enum("Estado", Estado, actual.estado)
            nueva_forma_pago = self.__pedir_enum("Forma de pago", FormaPago, actual.forma_pago)
            self.__pedido_servicio.actualizar(id_pedido, nuevo_estado, nueva_forma_pago)
            mostrar_exito(f"Pedido con ID {id_pedido} actualizado.")
        except FoodStoreError as e:
            mostrar_error(str(e))

    def __eliminar_pedido(self) -> None:
        """Elimina un pedido existente."""
        try:
            id_pedido = validar_numero("ID del pedido a eliminar: ")
            if validar_texto("Confirma eliminación? (S/N): ").upper() != "S":
                mostrar_info("Operación cancelada.")
                return
            self.__pedido_servicio.eliminar(id_pedido)
            mostrar_exito("Pedido eliminado.")
        except FoodStoreError as e:
            mostrar_error(str(e))
