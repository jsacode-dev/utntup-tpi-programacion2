from entidades.categoria import Categoria
from entidades.producto import Producto
from excepciones.food_store_error import EntidadNoEncontradaError
from servicios.categoria_servicio import CategoriaServicio

class ProductoServicio:
    def __init__(self, categoria_servicio: CategoriaServicio) -> None:
        self.__categoria_servicio = categoria_servicio
        self.__productos: list[Producto] = []

    def listar(self) -> list[Producto]:
        return [p for p in self.__productos if not p.eliminado]

    def listar_disponibles(self) -> list[Producto]:
        return [p for p in self.listar() if p.disponible and p.stock > 0]

    def filtrar_por_categoria(self, categoria: Categoria) -> list[Producto]: # Opcional. No se si dejarlo de forma definitiva o no.
        return [p for p in self.listar() if p.categoria == categoria]

    def buscar_por_id(self, id_producto: int) -> Producto:
        for p in self.__productos:
            if p.id == id_producto and not p.eliminado:
                return p
        raise EntidadNoEncontradaError(f"Producto con ID {id_producto} no encontrado.")

    def crear(self, nombre: str, descripcion: str, precio: float, stock: int, imagen: str, disponible: bool, id_categoria: int) -> Producto:
        categoria = self.__categoria_servicio.buscar_por_id(id_categoria)
        producto = Producto(nombre, descripcion, precio, stock, imagen, disponible, categoria)
        self.__productos.append(producto)
        return producto

    def editar(self, id_producto: int, nombre: str, descripcion: str, precio: float, stock: int, imagen: str, disponible: bool) -> Producto:
        producto = self.buscar_por_id(id_producto)
        producto.nombre = nombre
        producto.descripcion = descripcion
        producto.precio = precio
        producto.stock = stock
        producto.imagen = imagen
        producto.disponible = disponible
        return producto

    def eliminar(self, id_producto: int) -> None:
        producto = self.buscar_por_id(id_producto)
        producto.eliminado = True
