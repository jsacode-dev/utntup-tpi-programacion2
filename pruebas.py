from collections.abc import Callable

from entidades.usuario import Usuario
from enums.estado import Estado
from enums.forma_pago import FormaPago
from enums.rol import Rol
from excepciones.food_store_error import (
    CredencialesInvalidasError,
    DatoInvalidoError,
    DuplicadoError,
    EntidadNoEncontradaError,
    OperacionNoPermitidaError,
    PrecioInvalidoError,
    StockInsuficienteError,
)
from servicios.categoria_servicio import CategoriaServicio
from servicios.pedido_servicio import PedidoServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio

def verificar(descripcion: str, condicion: bool) -> None:
    print(f"{'OK    ' if condicion else 'FALLA '} {descripcion}")

def verificar_error(descripcion: str, excepcion: type[Exception], funcion: Callable[[], object]) -> None:
    try:
        funcion()
        verificar(descripcion, False)
    except excepcion:
        verificar(descripcion, True)

# Datos compartidos por todas las épicas
categoria_servicio = CategoriaServicio()
producto_servicio = ProductoServicio(categoria_servicio)
categoria = categoria_servicio.crear("Bebidas", "Sin alcohol")
usuario_servicio = UsuarioServicio()
admin = usuario_servicio.crear("Ana", "Pérez", "ana@mail.com", "1155550000", "admin123", Rol.ADMIN)
pedido_servicio = PedidoServicio(usuario_servicio, producto_servicio)

# Épica 0 - Acceso al sistema
def epica_0() -> None:
    verificar("autenticar con mail y contraseña correctos devuelve el usuario", usuario_servicio.autenticar("ana@mail.com", "admin123") is admin)
    verificar_error("contraseña incorrecta lanza CredencialesInvalidasError", CredencialesInvalidasError,
                    lambda: usuario_servicio.autenticar("ana@mail.com", "clave-mal"))
    verificar_error("mail inexistente lanza CredencialesInvalidasError", CredencialesInvalidasError,
                    lambda: usuario_servicio.autenticar("nadie@mail.com", "admin123"))

# Épica 1 - Gestión de categorías
def epica_1() -> None:
    verificar("listar incluye la categoría creada en los datos compartidos", categoria in categoria_servicio.listar())
    verificar_error("nombre repetido sin distinguir mayúsculas lanza DuplicadoError", DuplicadoError,
                    lambda: categoria_servicio.crear("bebidas", "Otra descripción"))
    verificar_error("nombre vacío lanza DatoInvalidoError", DatoInvalidoError,
                    lambda: categoria_servicio.crear("  ", "Sin nombre"))
    verificar_error("descripción vacía lanza DatoInvalidoError", DatoInvalidoError,
                    lambda: categoria_servicio.crear("Postres", " "))

    postres = categoria_servicio.crear("Postres", "Dulces")
    verificar("crear asigna id y la agrega a listar", postres.id >= 0 and postres in categoria_servicio.listar())

    verificar_error("editar con nombre de otra categoría lanza DuplicadoError", DuplicadoError,
                    lambda: categoria_servicio.editar(postres.id, "bebidas", "Dulces"))
    editada = categoria_servicio.editar(postres.id, "Postres", "Dulces y tortas")
    verificar("editar actualiza la descripción", editada.descripcion == "Dulces y tortas")
    verificar_error("editar una categoría inexistente lanza EntidadNoEncontradaError", EntidadNoEncontradaError,
                    lambda: categoria_servicio.editar(9999, "Inexistente", "Sin datos"))

    flan = producto_servicio.crear("Flan", "Casero", 1200.0, 3, "flan.jpg", True, postres.id)
    verificar_error("eliminar categoría con productos activos lanza OperacionNoPermitidaError", OperacionNoPermitidaError,
                    lambda: categoria_servicio.eliminar(postres.id))
    producto_servicio.eliminar(flan.id)
    categoria_servicio.eliminar(postres.id)
    verificar("eliminar oculta la categoría de listar", postres not in categoria_servicio.listar())
    verificar_error("buscar_por_id de una categoría eliminada lanza EntidadNoEncontradaError", EntidadNoEncontradaError,
                    lambda: categoria_servicio.buscar_por_id(postres.id))

# Épica 2 - Gestión de productos
def epica_2() -> None:
    producto = producto_servicio.crear("Agua", "Sin gas 500 ml", 1500.0, 10, "agua.jpg", True, categoria.id)
    verificar("crear asigna id y lo agrega a la categoría", producto.id >= 0 and producto in categoria.productos)
    verificar("listar_disponibles incluye producto disponible con stock", producto in producto_servicio.listar_disponibles())

    verificar_error("precio negativo lanza PrecioInvalidoError", PrecioInvalidoError,
                    lambda: producto_servicio.crear("Jugo", "Naranja", -1.0, 5, "jugo.jpg", True, categoria.id))
    verificar_error("stock negativo lanza DatoInvalidoError", DatoInvalidoError,
                    lambda: producto_servicio.crear("Jugo", "Naranja", 800.0, -1, "jugo.jpg", True, categoria.id))
    verificar_error("nombre vacío lanza DatoInvalidoError", DatoInvalidoError,
                    lambda: producto_servicio.crear("  ", "Naranja", 800.0, 5, "jugo.jpg", True, categoria.id))
    verificar_error("categoría inexistente lanza EntidadNoEncontradaError", EntidadNoEncontradaError,
                    lambda: producto_servicio.crear("Jugo", "Naranja", 800.0, 5, "jugo.jpg", True, 9999))

    sin_stock = producto_servicio.crear("Soda", "Limón", 900.0, 0, "soda.jpg", True, categoria.id)
    verificar("producto con stock 0 no aparece en listar_disponibles", sin_stock not in producto_servicio.listar_disponibles())

    producto_servicio.editar(producto.id, "Agua", "Sin gas 500 ml", 1800.0, 10, "agua.jpg", True)
    verificar("editar actualiza el precio", producto_servicio.buscar_por_id(producto.id).precio == 1800.0)

    producto_servicio.eliminar(producto.id)
    verificar("eliminar oculta el producto de listar", producto not in producto_servicio.listar())
    verificar_error("buscar_por_id de un producto eliminado lanza EntidadNoEncontradaError", EntidadNoEncontradaError,
                    lambda: producto_servicio.buscar_por_id(producto.id))

# Épica 3 - Gestión de usuarios
def epica_3() -> None:
    cliente = usuario_servicio.crear("Luis", "Gómez", "luis@mail.com", "1166660000", "cliente123", Rol.USUARIO)
    verificar("crear agrega el usuario a listar", cliente in usuario_servicio.listar())
    verificar_error("mail sin @ lanza DatoInvalidoError", DatoInvalidoError,
                    lambda: Usuario("Juan", "Ruiz", "juanmail.com", "1177770000", "clave", Rol.USUARIO))
    verificar_error("mail sin punto lanza DatoInvalidoError", DatoInvalidoError,
                    lambda: Usuario("Juan", "Ruiz", "juan@mailcom", "1177770000", "clave", Rol.USUARIO))
    verificar_error("mail duplicado sin distinguir mayúsculas lanza DuplicadoError", DuplicadoError,
                    lambda: usuario_servicio.crear("Otra", "Persona", "ANA@mail.com", "1188880000", "clave", Rol.USUARIO))
    verificar_error("editar con mail de otro usuario lanza DuplicadoError", DuplicadoError,
                    lambda: usuario_servicio.editar(cliente.id, admin.id, "Luis", "Gómez", "ana@mail.com", "1166660000", Rol.USUARIO))
    editado = usuario_servicio.editar(cliente.id, admin.id, "Luis Alberto", "Gómez", "luis@mail.com", "1166669999", Rol.USUARIO)
    verificar("editar con su mismo mail actualiza el nombre", editado.nombre == "Luis Alberto")
    verificar_error("cambiar el propio rol lanza OperacionNoPermitidaError", OperacionNoPermitidaError,
                    lambda: usuario_servicio.editar(admin.id, admin.id, "Ana", "Pérez", "ana@mail.com", "1155550000", Rol.USUARIO))
    verificar_error("eliminarse a sí mismo lanza OperacionNoPermitidaError", OperacionNoPermitidaError,
                    lambda: usuario_servicio.eliminar(admin.id, admin.id))
    usuario_servicio.eliminar(cliente.id, admin.id)
    verificar("eliminar oculta el usuario de listar", cliente not in usuario_servicio.listar())
    verificar_error("autenticar un usuario eliminado lanza CredencialesInvalidasError", CredencialesInvalidasError,
                    lambda: usuario_servicio.autenticar("luis@mail.com", "cliente123"))
    verificar_error("buscar_por_id de un usuario eliminado lanza EntidadNoEncontradaError", EntidadNoEncontradaError,
                    lambda: usuario_servicio.buscar_por_id(cliente.id))

# Épica 4 - Gestión de pedidos y detalles
def epica_4() -> None:
    marta = usuario_servicio.crear("Marta", "Díaz", "marta@mail.com", "1199990000", "marta123", Rol.USUARIO)
    otro = usuario_servicio.crear("Otro", "Cliente", "otro@mail.com", "1122223333", "otro123", Rol.USUARIO)
    jugo = producto_servicio.crear("Jugo", "Naranja", 800.0, 5, "jugo.jpg", True, categoria.id)
    agua_pedidos = producto_servicio.crear("Agua", "Sin gas", 1500.0, 10, "agua.jpg", True, categoria.id)
    no_disponible = producto_servicio.crear("Té", "Frío", 700.0, 5, "te.jpg", False, categoria.id)

    p1 = pedido_servicio.crear(marta.id, FormaPago.EFECTIVO, [(jugo.id, 2)])
    verificar("crear pedido arranca PENDIENTE y calcula el total", p1.estado == Estado.PENDIENTE and p1.total == 1600.0)
    verificar("crear pedido descuenta el stock (5 - 2 = 3)", jugo.stock == 3)

    listados_antes = len(pedido_servicio.listar())
    verificar_error("pedido con cantidades que superan el stock lanza StockInsuficienteError", StockInsuficienteError,
                    lambda: pedido_servicio.crear(marta.id, FormaPago.EFECTIVO, [(jugo.id, 1), (jugo.id, 10)]))
    verificar("pedido fallido no se guarda y no modifica el stock",
                len(pedido_servicio.listar()) == listados_antes and jugo.stock == 3)

    p2 = pedido_servicio.crear(marta.id, FormaPago.TARJETA, [(agua_pedidos.id, 1), (agua_pedidos.id, 2)])
    verificar("productos repetidos se suman en un solo detalle", len(p2.detalles) == 1 and p2.detalles[0].cantidad == 3)
    verificar("subtotal y total del detalle repetido son correctos", p2.total == 4500.0)
    verificar("stock se descuenta con la cantidad total (10 - 3 = 7)", agua_pedidos.stock == 7)

    verificar_error("cantidad 0 lanza DatoInvalidoError", DatoInvalidoError,
                    lambda: pedido_servicio.crear(marta.id, FormaPago.EFECTIVO, [(jugo.id, 0)]))
    verificar_error("producto no disponible lanza OperacionNoPermitidaError", OperacionNoPermitidaError,
                    lambda: pedido_servicio.crear(marta.id, FormaPago.EFECTIVO, [(no_disponible.id, 1)]))
    producto_borrado = producto_servicio.crear("Tmp", "x", 10.0, 5, "t.jpg", True, categoria.id)
    producto_servicio.eliminar(producto_borrado.id)
    verificar_error("producto eliminado lanza EntidadNoEncontradaError", EntidadNoEncontradaError,
                    lambda: pedido_servicio.crear(marta.id, FormaPago.EFECTIVO, [(producto_borrado.id, 1)]))

    temporal = usuario_servicio.crear("Temp", "Demo", "temp@mail.com", "1100000000", "temp123", Rol.USUARIO)
    usuario_servicio.eliminar(temporal.id, admin.id)
    verificar_error("pedido de usuario eliminado lanza EntidadNoEncontradaError", EntidadNoEncontradaError,
                    lambda: pedido_servicio.crear(temporal.id, FormaPago.EFECTIVO, [(jugo.id, 1)]))

    pedido_servicio.actualizar(p1.id, Estado.CONFIRMADO)
    verificar("transición PENDIENTE -> CONFIRMADO es válida", pedido_servicio.buscar_por_id(p1.id).estado == Estado.CONFIRMADO)
    pedido_servicio.actualizar(p1.id, Estado.TERMINADO)
    verificar("transición CONFIRMADO -> TERMINADO es válida", pedido_servicio.buscar_por_id(p1.id).estado == Estado.TERMINADO)
    verificar_error("transición TERMINADO -> CANCELADO lanza OperacionNoPermitidaError", OperacionNoPermitidaError,
                    lambda: pedido_servicio.actualizar(p1.id, Estado.CANCELADO))

    p3 = pedido_servicio.crear(marta.id, FormaPago.EFECTIVO, [(jugo.id, 1)])
    verificar("stock baja a 2 con el pedido p3", jugo.stock == 2)
    pedido_servicio.actualizar(p3.id, Estado.CANCELADO)
    verificar("cancelar un pedido devuelve el stock (2 + 1 = 3)", jugo.stock == 3)

    p4 = pedido_servicio.crear(marta.id, FormaPago.EFECTIVO, [(jugo.id, 1)])
    verificar_error("transición PENDIENTE -> TERMINADO lanza OperacionNoPermitidaError", OperacionNoPermitidaError,
                    lambda: pedido_servicio.actualizar(p4.id, Estado.TERMINADO))
    pedido_servicio.eliminar(p4.id)
    verificar("eliminar pedido PENDIENTE devuelve el stock (3)", jugo.stock == 3)
    verificar("eliminar oculta el pedido de listar", p4 not in pedido_servicio.listar())

    pedido_servicio.eliminar(p1.id)
    verificar("eliminar pedido TERMINADO no devuelve el stock (sigue en 3)", jugo.stock == 3)

    verificar("listar_de_usuario devuelve solo los pedidos vigentes de ese usuario",
                p2 in pedido_servicio.listar_de_usuario(marta) and p1 not in pedido_servicio.listar_de_usuario(marta))
    verificar_error("buscar_de_usuario con pedido de otro usuario lanza EntidadNoEncontradaError", EntidadNoEncontradaError,
                    lambda: pedido_servicio.buscar_de_usuario(p2.id, otro))
    verificar("buscar_de_usuario con pedido propio lo devuelve", pedido_servicio.buscar_de_usuario(p2.id, marta) is p2)

# Filtros opcionales (listar por categoría y por usuario)
def filtros_opcionales() -> None:
    snacks = categoria_servicio.crear("Snacks", "Para picar")
    vacia = categoria_servicio.crear("Vacía", "Sin productos")
    papas = producto_servicio.crear("Papas", "Fritas", 1000.0, 4, "papas.jpg", True, snacks.id)
    papas_sin_stock = producto_servicio.crear("Nachos", "Con queso", 1100.0, 0, "nachos.jpg", True, snacks.id)
    papas_no_disp = producto_servicio.crear("Maní", "Salado", 600.0, 3, "mani.jpg", False, snacks.id)
    papas_borrada = producto_servicio.crear("Chizitos", "Bolsa", 500.0, 2, "chizitos.jpg", True, snacks.id)
    producto_servicio.eliminar(papas_borrada.id)

    verificar("listar(categoria) incluye solo productos de esa categoría", papas in producto_servicio.listar(snacks) and all(p.categoria == snacks for p in producto_servicio.listar(snacks)))
    verificar("listar(categoria) no incluye productos de otra categoría", not any(p.categoria == categoria for p in producto_servicio.listar(snacks)))
    verificar("listar(categoria) excluye productos eliminados", papas_borrada not in producto_servicio.listar(snacks))
    verificar("listar(categoria sin productos) devuelve lista vacía", producto_servicio.listar(vacia) == [])
    verificar("listar() sin filtro devuelve los mismos que listar(None)", producto_servicio.listar() == producto_servicio.listar(None))
    verificar("listar_disponibles(categoria) incluye productos disponibles con stock", papas in producto_servicio.listar_disponibles(snacks))
    verificar("listar_disponibles(categoria) excluye productos sin stock", papas_sin_stock not in producto_servicio.listar_disponibles(snacks))
    verificar("listar_disponibles(categoria) excluye productos no disponibles", papas_no_disp not in producto_servicio.listar_disponibles(snacks))
    verificar("listar_disponibles(None) incluye productos de todas las categorías", papas in producto_servicio.listar_disponibles(None) and producto_servicio.listar_disponibles() == producto_servicio.listar_disponibles(None))

    cliente_filtro = usuario_servicio.crear("Filtro", "Uno", "filtro1@mail.com", "1133330000", "filtro123", Rol.USUARIO)
    cliente_sin_pedidos = usuario_servicio.crear("Filtro", "Dos", "filtro2@mail.com", "1144440000", "filtro123", Rol.USUARIO)
    pedido_visible = pedido_servicio.crear(cliente_filtro.id, FormaPago.EFECTIVO, [(papas.id, 1)])
    pedido_eliminado = pedido_servicio.crear(cliente_filtro.id, FormaPago.EFECTIVO, [(papas.id, 1)])
    pedido_servicio.eliminar(pedido_eliminado.id)

    verificar("listar(usuario) incluye solo pedidos de ese usuario", pedido_visible in pedido_servicio.listar(cliente_filtro) and all(p.usuario == cliente_filtro for p in pedido_servicio.listar(cliente_filtro)))
    verificar("listar(usuario) excluye pedidos eliminados", pedido_eliminado not in pedido_servicio.listar(cliente_filtro))
    verificar("listar(usuario sin pedidos) devuelve lista vacía", pedido_servicio.listar(cliente_sin_pedidos) == [])
    verificar("pedidos listar() sin filtro devuelve los mismos que listar(None)", pedido_servicio.listar() == pedido_servicio.listar(None))

epica_0()
epica_1()
epica_2()
epica_3()
epica_4()
filtros_opcionales()
