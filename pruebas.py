from excepciones.food_store_error import DatoInvalidoError, EntidadNoEncontradaError, PrecioInvalidoError
from servicios.categoria_servicio import CategoriaServicio
from servicios.producto_servicio import ProductoServicio

def verificar(descripcion: str, condicion: bool) -> None:
    print(f"{'OK    ' if condicion else 'FALLA '} {descripcion}")

def verificar_error(descripcion: str, excepcion: type[Exception], funcion: callable) -> None:
    try:
        funcion()
        verificar(descripcion, False)
    except excepcion:
        verificar(descripcion, True)

categoria_servicio = CategoriaServicio()
producto_servicio = ProductoServicio(categoria_servicio)
categoria = categoria_servicio.crear("Bebidas", "Sin alcohol")

producto = producto_servicio.crear("Agua", "Sin gas 500 ml", 1500.0, 10, "agua.jpg", True, categoria.id)
verificar("crear asigna id y lo agrega a la categoría", producto.id > 0 and producto in categoria.productos)
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
