from entidades.categoria import Categoria
from entidades.producto import Producto
from excepciones.food_store_error import EntidadNoEncontradaError
from servicios.categoria_servicio import CategoriaServicio

class ProductoServicio:
    """Servicio de gestión de productos con filtrado por disponibilidad y categoría."""

    def __init__(self, categoria_servicio: CategoriaServicio) -> None:
        self.__categoria_servicio = categoria_servicio
        self.__productos: list[Producto] = []

    def listar(self, categoria: Categoria | None = None) -> list[Producto]:
        """Retorna todos los productos activos, opcionalmente filtrados por categoría."""
        return [p for p in self.__productos if not p.eliminado and (categoria is None or p.categoria == categoria)]

    def listar_disponibles(self, categoria: Categoria | None = None) -> list[Producto]:
        """Retorna productos activos, disponibles y con stock, opcionalmente filtrados por categoría."""
        return [p for p in self.listar(categoria) if p.disponible and p.stock > 0]

    def buscar_por_id(self, id_producto: int) -> Producto:
        """Busca un producto por su ID."""
        for p in self.__productos:
            if p.id == id_producto and not p.eliminado:
                return p
        raise EntidadNoEncontradaError(f"Producto con ID {id_producto} no encontrado.")

    def crear(self, nombre: str, descripcion: str, precio: float, stock: int, imagen: str, disponible: bool, id_categoria: int) -> Producto:
        """Crea un nuevo producto asignado a una categoría."""
        categoria = self.__categoria_servicio.buscar_por_id(id_categoria)
        producto = Producto(nombre, descripcion, precio, stock, imagen, disponible, categoria)
        self.__productos.append(producto)
        return producto

    def editar(self, id_producto: int, nombre: str, descripcion: str, precio: float, stock: int, imagen: str, disponible: bool) -> Producto:
        """Edita los datos de un producto existente."""
        producto = self.buscar_por_id(id_producto)
        producto.nombre = nombre
        producto.descripcion = descripcion
        producto.precio = precio
        producto.stock = stock
        producto.imagen = imagen
        producto.disponible = disponible
        return producto

    def eliminar(self, id_producto: int) -> None:
        """Elimina un producto (soft delete)."""
        producto = self.buscar_por_id(id_producto)
        producto.eliminado = True
