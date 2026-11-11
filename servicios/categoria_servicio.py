from entidades.categoria import Categoria
from excepciones.food_store_error import EntidadNoEncontradaError, DuplicadoError, OperacionNoPermitidaError

class CategoriaServicio:
    """Servicio de gestión de categorías con validación de unicidad."""

    def __init__(self) -> None:
        self.__categorias: list[Categoria] = []

    def listar(self) -> list[Categoria]:
        """Retorna todas las categorías activas."""
        return [c for c in self.__categorias if not c.eliminado]

    def buscar_por_id(self, id_categoria: int) -> Categoria:
        """Busca una categoría por su ID."""
        for categoria in self.__categorias:
            if categoria.id == id_categoria and not categoria.eliminado:
                return categoria
        raise EntidadNoEncontradaError(f"No existe una categoría con ID {id_categoria}")

    def crear(self, nombre: str, descripcion: str) -> Categoria:
        """Crea una nueva categoría con validación de unicidad."""
        self.__validar_nombre_unico(nombre)
        categoria = Categoria(nombre, descripcion)
        self.__categorias.append(categoria)
        return categoria

    def editar(self, id_categoria: int, nombre: str, descripcion: str) -> Categoria:
        """Edita los datos de una categoría existente."""
        categoria = self.buscar_por_id(id_categoria)
        self.__validar_nombre_unico(nombre, id_categoria)
        categoria.nombre = nombre
        categoria.descripcion = descripcion
        return categoria

    def eliminar(self, id_categoria: int) -> None:
        """Elimina una categoría si no tiene productos activos."""
        categoria = self.buscar_por_id(id_categoria)
        activos = len([p for p in categoria.productos if not p.eliminado])
        if activos > 0:
            raise OperacionNoPermitidaError(
                f"No se puede eliminar: la categoría tiene {activos} producto(s) activo(s)"
            )
        categoria.eliminado = True

    def __validar_nombre_unico(self, nombre: str, id_excluido: int | None = None) -> None:
        """Valida que el nombre de la categoría sea único (sin distinguir mayúsculas)."""
        for categoria in self.listar():
            if categoria.nombre.lower() == nombre.strip().lower() and categoria.id != id_excluido:
                raise DuplicadoError(f"Ya existe una categoría llamada {categoria.nombre}")
